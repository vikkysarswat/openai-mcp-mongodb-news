#!/usr/bin/env python3
"""
MCP Server with MongoDB Integration for ChatGPT Connector
Implements fetch_news tool to pull news from MongoDB and display via widgets
"""

import asyncio
import os
from typing import Any, Optional
from datetime import datetime

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("mongodb-news-mcp")

# MongoDB connection
db_client: Optional[MongoClient] = None
db = None
news_collection = None


def connect_to_mongodb():
    """Establish connection to MongoDB"""
    global db_client, db, news_collection
    
    try:
        # Get MongoDB connection string from environment variable
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGODB_DATABASE", "news_db")
        collection_name = os.getenv("MONGODB_COLLECTION", "news")
        
        logger.info(f"Connecting to MongoDB at {mongo_uri}")
        db_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Verify connection
        db_client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        db = db_client[db_name]
        news_collection = db[collection_name]
        
        return True
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return False
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return False


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="fetch_news",
            description="Fetch news articles from MongoDB collection. Returns news with title, content, source, and published date. Supports filtering by category, date range, and limit.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter news by category (e.g., technology, sports, business, entertainment)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of news articles to return (default: 10)",
                        "default": 10
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["date", "relevance"],
                        "description": "Sort order for results (default: date)",
                        "default": "date"
                    },
                    "days_back": {
                        "type": "integer",
                        "description": "Fetch news from last N days (default: 7)",
                        "default": 7
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="search_news",
            description="Search news articles by keywords in title or content",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find in news title or content"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["query"]
            },
        ),
        types.Tool(
            name="get_news_categories",
            description="Get list of available news categories from the database",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests"""
    
    if not news_collection:
        return [types.TextContent(
            type="text",
            text="Error: MongoDB connection not established. Please check your connection settings."
        )]
    
    try:
        if name == "fetch_news":
            return await fetch_news_handler(arguments or {})
        elif name == "search_news":
            return await search_news_handler(arguments or {})
        elif name == "get_news_categories":
            return await get_categories_handler()
        else:
            return [types.TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error executing tool: {str(e)}"
        )]


async def fetch_news_handler(arguments: dict) -> list[types.TextContent]:
    """Fetch news from MongoDB based on filters"""
    category = arguments.get("category")
    limit = arguments.get("limit", 10)
    sort_by = arguments.get("sort_by", "date")
    days_back = arguments.get("days_back", 7)
    
    # Build query
    query = {}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    
    # Add date filter
    from datetime import timedelta
    cutoff_date = datetime.now() - timedelta(days=days_back)
    query["published_date"] = {"$gte": cutoff_date}
    
    # Determine sort order
    sort_field = "published_date" if sort_by == "date" else "_id"
    
    try:
        # Fetch from MongoDB
        cursor = news_collection.find(query).sort(sort_field, -1).limit(limit)
        news_articles = list(cursor)
        
        if not news_articles:
            return [types.TextContent(
                type="text",
                text=f"No news articles found matching the criteria. Category: {category or 'all'}, Days back: {days_back}"
            )]
        
        # Format results for widget display
        result = format_news_for_widget(news_articles, category)
        
        return [types.TextContent(
            type="text",
            text=result
        )]
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error fetching news from database: {str(e)}"
        )]


async def search_news_handler(arguments: dict) -> list[types.TextContent]:
    """Search news by keywords"""
    query_text = arguments.get("query", "")
    limit = arguments.get("limit", 10)
    
    if not query_text:
        return [types.TextContent(
            type="text",
            text="Please provide a search query."
        )]
    
    try:
        # Search in title and content
        query = {
            "$or": [
                {"title": {"$regex": query_text, "$options": "i"}},
                {"content": {"$regex": query_text, "$options": "i"}}
            ]
        }
        
        cursor = news_collection.find(query).sort("published_date", -1).limit(limit)
        news_articles = list(cursor)
        
        if not news_articles:
            return [types.TextContent(
                type="text",
                text=f"No news articles found for query: '{query_text}'"
            )]
        
        result = format_news_for_widget(news_articles, f"Search: {query_text}")
        
        return [types.TextContent(
            type="text",
            text=result
        )]
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error searching news: {str(e)}"
        )]


async def get_categories_handler() -> list[types.TextContent]:
    """Get distinct categories from news collection"""
    try:
        categories = news_collection.distinct("category")
        
        if not categories:
            return [types.TextContent(
                type="text",
                text="No categories found in the database."
            )]
        
        result = "Available News Categories:\n\n"
        for idx, category in enumerate(categories, 1):
            result += f"{idx}. {category}\n"
        
        return [types.TextContent(
            type="text",
            text=result
        )]
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error fetching categories: {str(e)}"
        )]


def format_news_for_widget(news_articles: list, title: str = "News Feed") -> str:
    """
    Format news articles for widget display in ChatGPT
    Similar to the pizza example widget format
    """
    result = f"📰 **{title}**\n\n"
    result += f"Found {len(news_articles)} article(s)\n\n"
    result += "=" * 60 + "\n\n"
    
    for idx, article in enumerate(news_articles, 1):
        title = article.get("title", "Untitled")
        content = article.get("content", "No content available")
        source = article.get("source", "Unknown source")
        category = article.get("category", "Uncategorized")
        published_date = article.get("published_date", datetime.now())
        url = article.get("url", "")
        
        # Format date
        if isinstance(published_date, datetime):
            date_str = published_date.strftime("%B %d, %Y %I:%M %p")
        else:
            date_str = str(published_date)
        
        # Truncate content for preview
        content_preview = content[:200] + "..." if len(content) > 200 else content
        
        result += f"**{idx}. {title}**\n"
        result += f"📂 Category: {category}\n"
        result += f"📰 Source: {source}\n"
        result += f"📅 Published: {date_str}\n\n"
        result += f"{content_preview}\n\n"
        
        if url:
            result += f"🔗 Read more: {url}\n\n"
        
        result += "-" * 60 + "\n\n"
    
    return result


async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting MongoDB News MCP Server...")
    
    # Connect to MongoDB
    if not connect_to_mongodb():
        logger.error("Failed to connect to MongoDB. Please check your configuration.")
        logger.info("Server will start but tools will not function properly.")
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("MCP Server is running...")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mongodb-news-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
