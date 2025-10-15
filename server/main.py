#!/usr/bin/env python3
"""
OpenAI Apps SDK MCP Server with MongoDB Integration
Based on the pizza example from openai-apps-sdk-examples
"""

import os
import json
from typing import Any, Dict, List
from datetime import datetime, timedelta

from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
db_client = None
db = None
news_collection = None

# Asset URLs for widgets (you'll host these)
ASSET_BASE_URL = os.getenv("ASSET_BASE_URL", "http://localhost:4444")


def connect_to_mongodb():
    """Establish connection to MongoDB"""
    global db_client, db, news_collection
    
    try:
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
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return False


# Initialize MongoDB connection
connect_to_mongodb()

# Initialize FastMCP with HTTP transport for Apps SDK
mcp = FastMCP(
    name="mongodb-news",
    sse_path="/mcp",
    message_path="/mcp/messages"
)


# Define widget templates
class NewsWidget:
    def __init__(self, identifier: str, title: str, template_uri: str, html: str,
                 invoking: str = "Loading news...", invoked: str = "News loaded"):
        self.identifier = identifier
        self.title = title
        self.template_uri = template_uri
        self.html = html
        self.invoking = invoking
        self.invoked = invoked


# Widget definitions
widgets = [
    NewsWidget(
        identifier="news-list",
        title="News Feed",
        template_uri="ui://widget/news-list.html",
        html=(
            '<div id="news-list-root"></div>\n'
            f'<link rel="stylesheet" href="{ASSET_BASE_URL}/news-list.css">\n'
            f'<script type="module" src="{ASSET_BASE_URL}/news-list.js"></script>'
        ),
        invoking="Fetching news articles...",
        invoked="Here are your news articles"
    ),
    NewsWidget(
        identifier="news-search",
        title="Search Results",
        template_uri="ui://widget/news-search.html",
        html=(
            '<div id="news-search-root"></div>\n'
            f'<link rel="stylesheet" href="{ASSET_BASE_URL}/news-search.css">\n'
            f'<script type="module" src="{ASSET_BASE_URL}/news-search.js"></script>'
        ),
        invoking="Searching news...",
        invoked="Search complete"
    )
]

WIDGETS_BY_ID: Dict[str, NewsWidget] = {widget.identifier: widget for widget in widgets}
WIDGETS_BY_URI: Dict[str, NewsWidget] = {widget.template_uri: widget for widget in widgets}

MIME_TYPE = "text/html+skybridge"


# Pydantic models for tool inputs
class FetchNewsInput(BaseModel):
    """Schema for fetch_news tool."""
    category: str = Field(
        default="",
        description="Filter news by category (e.g., Technology, Business, Sports)"
    )
    limit: int = Field(
        default=10,
        description="Maximum number of articles to return"
    )
    days_back: int = Field(
        default=7,
        alias="daysBack",
        description="Fetch news from last N days"
    )
    
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class SearchNewsInput(BaseModel):
    """Schema for search_news tool."""
    query: str = Field(
        ...,
        description="Search query to find in news title or content"
    )
    limit: int = Field(
        default=10,
        description="Maximum number of results to return"
    )
    
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


# Register resources (widgets)
@mcp.resource("ui://widget/news-list.html")
def news_list_widget() -> str:
    """News list widget resource"""
    widget = WIDGETS_BY_URI["ui://widget/news-list.html"]
    return widget.html


@mcp.resource("ui://widget/news-search.html")
def news_search_widget() -> str:
    """News search widget resource"""
    widget = WIDGETS_BY_URI["ui://widget/news-search.html"]
    return widget.html


def _embedded_widget_resource(widget: NewsWidget) -> Dict[str, Any]:
    """Create embedded widget resource for metadata"""
    return {
        "uri": widget.template_uri,
        "mimeType": MIME_TYPE,
        "text": widget.html
    }


@mcp.tool()
def fetch_news(
    category: str = "",
    limit: int = 10,
    days_back: int = 7
) -> dict:
    """
    Fetch news articles from MongoDB.
    
    Args:
        category: Filter by category (optional)
        limit: Maximum number of articles (default 10)
        days_back: Fetch news from last N days (default 7)
    
    Returns:
        Structured news data with widget metadata
    """
    if not news_collection:
        return {
            "text": "Error: MongoDB connection not established",
            "data": {"error": "Database not connected"}
        }
    
    try:
        # Build query
        query = {}
        if category:
            query["category"] = {"$regex": category, "$options": "i"}
        
        # Add date filter
        cutoff_date = datetime.now() - timedelta(days=days_back)
        query["published_date"] = {"$gte": cutoff_date}
        
        # Fetch from MongoDB
        cursor = news_collection.find(query).sort("published_date", -1).limit(limit)
        articles = list(cursor)
        
        # Convert ObjectId to string
        for article in articles:
            article["_id"] = str(article["_id"])
            if isinstance(article.get("published_date"), datetime):
                article["published_date"] = article["published_date"].isoformat()
        
        widget = WIDGETS_BY_ID["news-list"]
        widget_resource = _embedded_widget_resource(widget)
        
        # Build response with widget metadata
        result = {
            "text": f"Found {len(articles)} news articles" + (f" in category '{category}'" if category else ""),
            "data": {
                "articles": articles,
                "category": category or "All",
                "count": len(articles),
                "days_back": days_back
            },
            "_meta": {
                "openai.com/widget": widget_resource,
                "openai/outputTemplate": widget.template_uri,
                "openai/toolInvocation/invoking": widget.invoking,
                "openai/toolInvocation/invoked": widget.invoked,
                "openai/widgetAccessible": True,
                "openai/widgetDescription": f"Displays {len(articles)} news articles" + (f" from {category}" if category else "")
            }
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return {
            "text": f"Error fetching news: {str(e)}",
            "data": {"error": str(e)}
        }


@mcp.tool()
def search_news(query: str, limit: int = 10) -> dict:
    """
    Search news articles by keywords.
    
    Args:
        query: Search query for title or content
        limit: Maximum number of results (default 10)
    
    Returns:
        Structured search results with widget metadata
    """
    if not news_collection:
        return {
            "text": "Error: MongoDB connection not established",
            "data": {"error": "Database not connected"}
        }
    
    if not query:
        return {
            "text": "Please provide a search query",
            "data": {"error": "No query provided"}
        }
    
    try:
        # Search in title and content
        search_query = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"content": {"$regex": query, "$options": "i"}}
            ]
        }
        
        cursor = news_collection.find(search_query).sort("published_date", -1).limit(limit)
        articles = list(cursor)
        
        # Convert ObjectId to string
        for article in articles:
            article["_id"] = str(article["_id"])
            if isinstance(article.get("published_date"), datetime):
                article["published_date"] = article["published_date"].isoformat()
        
        widget = WIDGETS_BY_ID["news-search"]
        widget_resource = _embedded_widget_resource(widget)
        
        result = {
            "text": f"Found {len(articles)} articles matching '{query}'",
            "data": {
                "articles": articles,
                "query": query,
                "count": len(articles)
            },
            "_meta": {
                "openai.com/widget": widget_resource,
                "openai/outputTemplate": widget.template_uri,
                "openai/toolInvocation/invoking": widget.invoking,
                "openai/toolInvocation/invoked": widget.invoked,
                "openai/widgetAccessible": True,
                "openai/widgetDescription": f"Search results for '{query}' - {len(articles)} articles found"
            }
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error searching news: {e}")
        return {
            "text": f"Error searching news: {str(e)}",
            "data": {"error": str(e)}
        }


@mcp.tool()
def get_news_categories() -> dict:
    """
    Get list of available news categories.
    
    Returns:
        List of categories with article counts
    """
    if not news_collection:
        return {
            "text": "Error: MongoDB connection not established",
            "data": {"error": "Database not connected"}
        }
    
    try:
        # Get distinct categories with counts
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        results = list(news_collection.aggregate(pipeline))
        categories = [{"name": r["_id"], "count": r["count"]} for r in results]
        
        return {
            "text": f"Found {len(categories)} categories",
            "data": {
                "categories": categories,
                "total": len(categories)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return {
            "text": f"Error getting categories: {str(e)}",
            "data": {"error": str(e)}
        }


# Get the FastAPI app for deployment
app = mcp.get_app()

# Add CORS middleware for development
try:
    from starlette.middleware.cors import CORSMiddleware
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
    )
except Exception:
    pass


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting MongoDB News MCP Server with Apps SDK...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
