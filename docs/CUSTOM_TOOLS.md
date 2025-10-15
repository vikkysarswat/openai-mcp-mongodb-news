# Creating Custom Tools - Examples

This guide shows you how to add custom tools to your MCP server with practical examples.

## 📋 Table of Contents

1. [Basic Tool Template](#basic-tool-template)
2. [Example 1: Add News Tool](#example-1-add-news-tool)
3. [Example 2: Delete News Tool](#example-2-delete-news-tool)
4. [Example 3: News Statistics Tool](#example-3-news-statistics-tool)
5. [Example 4: Trending Topics Tool](#example-4-trending-topics-tool)
6. [Example 5: RSS Feed Importer](#example-5-rss-feed-importer)

---

## Basic Tool Template

Every tool requires three components:

### 1. Tool Definition (in `handle_list_tools()`)

```python
types.Tool(
    name="tool_name",
    description="Clear description of what the tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"]
    },
)
```

### 2. Tool Handler Routing (in `handle_call_tool()`)

```python
elif name == "tool_name":
    return await tool_name_handler(arguments or {})
```

### 3. Tool Implementation

```python
async def tool_name_handler(arguments: dict) -> list[types.TextContent]:
    param1 = arguments.get("param1")
    
    # Your logic here
    
    return [types.TextContent(
        type="text",
        text="Result"
    )]
```

---

## Example 1: Add News Tool

Allow users to add news articles to the database.

### Step 1: Add to `handle_list_tools()`

```python
types.Tool(
    name="add_news",
    description="Add a new news article to the database",
    inputSchema={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Article title"
            },
            "content": {
                "type": "string",
                "description": "Article content/body"
            },
            "category": {
                "type": "string",
                "description": "Article category (e.g., Technology, Business)"
            },
            "source": {
                "type": "string",
                "description": "News source name"
            },
            "url": {
                "type": "string",
                "description": "Article URL (optional)"
            }
        },
        "required": ["title", "content", "category", "source"]
    },
)
```

### Step 2: Add routing

```python
elif name == "add_news":
    return await add_news_handler(arguments or {})
```

### Step 3: Implement handler

```python
async def add_news_handler(arguments: dict) -> list[types.TextContent]:
    """Add a new news article to MongoDB"""
    title = arguments.get("title")
    content = arguments.get("content")
    category = arguments.get("category")
    source = arguments.get("source")
    url = arguments.get("url", "")
    
    # Validate required fields
    if not all([title, content, category, source]):
        return [types.TextContent(
            type="text",
            text="Error: Missing required fields. Please provide title, content, category, and source."
        )]
    
    try:
        # Create article document
        article = {
            "title": title,
            "content": content,
            "category": category,
            "source": source,
            "url": url,
            "published_date": datetime.now()
        }
        
        # Insert into MongoDB
        result = news_collection.insert_one(article)
        
        return [types.TextContent(
            type="text",
            text=f"✅ Successfully added news article!\\n\\n"
                 f"**Title:** {title}\\n"
                 f"**Category:** {category}\\n"
                 f"**Source:** {source}\\n"
                 f"**ID:** {result.inserted_id}"
        )]
    except Exception as e:
        logger.error(f"Error adding news: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error adding news article: {str(e)}"
        )]
```

### Usage in ChatGPT

```
"Add a news article with title 'New AI Model Released', 
content 'A revolutionary AI model...', category 'Technology', 
and source 'Tech News'"
```

---

## Example 2: Delete News Tool

Allow users to delete news articles.

### Implementation

```python
# In handle_list_tools()
types.Tool(
    name="delete_news",
    description="Delete a news article by its ID",
    inputSchema={
        "type": "object",
        "properties": {
            "article_id": {
                "type": "string",
                "description": "MongoDB ObjectId of the article to delete"
            }
        },
        "required": ["article_id"]
    },
)

# Handler
async def delete_news_handler(arguments: dict) -> list[types.TextContent]:
    """Delete a news article from MongoDB"""
    from bson import ObjectId
    
    article_id = arguments.get("article_id")
    
    if not article_id:
        return [types.TextContent(
            type="text",
            text="Error: Please provide an article ID."
        )]
    
    try:
        # Convert string to ObjectId
        obj_id = ObjectId(article_id)
        
        # First check if article exists
        article = news_collection.find_one({"_id": obj_id})
        if not article:
            return [types.TextContent(
                type="text",
                text=f"❌ Article not found with ID: {article_id}"
            )]
        
        # Delete the article
        result = news_collection.delete_one({"_id": obj_id})
        
        if result.deleted_count > 0:
            return [types.TextContent(
                type="text",
                text=f"✅ Successfully deleted article:\\n\\n"
                     f"**Title:** {article['title']}\\n"
                     f"**Category:** {article['category']}"
            )]
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Failed to delete article with ID: {article_id}"
            )]
            
    except Exception as e:
        logger.error(f"Error deleting news: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error deleting article: {str(e)}"
        )]
```

---

## Example 3: News Statistics Tool

Get statistics about your news database.

### Implementation

```python
# In handle_list_tools()
types.Tool(
    name="get_news_stats",
    description="Get statistics about news articles in the database",
    inputSchema={
        "type": "object",
        "properties": {},
        "required": []
    },
)

# Handler
async def get_news_stats_handler(arguments: dict) -> list[types.TextContent]:
    """Get news database statistics"""
    try:
        # Total articles
        total = news_collection.count_documents({})
        
        # Count by category
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        category_counts = list(news_collection.aggregate(pipeline))
        
        # Count by source
        pipeline = [
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        top_sources = list(news_collection.aggregate(pipeline))
        
        # Recent articles (last 7 days)
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=7)
        recent_count = news_collection.count_documents({
            "published_date": {"$gte": cutoff}
        })
        
        # Build response
        result = "📊 **News Database Statistics**\\n\\n"
        result += f"**Total Articles:** {total}\\n"
        result += f"**Recent (Last 7 Days):** {recent_count}\\n\\n"
        
        result += "**Articles by Category:**\\n"
        for item in category_counts:
            result += f"  • {item['_id']}: {item['count']}\\n"
        
        result += "\\n**Top Sources:**\\n"
        for item in top_sources:
            result += f"  • {item['_id']}: {item['count']}\\n"
        
        return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error getting statistics: {str(e)}"
        )]
```

---

## Example 4: Trending Topics Tool

Analyze trending topics from news articles.

### Implementation

```python
# In handle_list_tools()
types.Tool(
    name="get_trending_topics",
    description="Analyze and get trending topics from recent news",
    inputSchema={
        "type": "object",
        "properties": {
            "days_back": {
                "type": "integer",
                "description": "Analyze news from last N days (default: 7)",
                "default": 7
            },
            "limit": {
                "type": "integer",
                "description": "Number of trending topics to return (default: 10)",
                "default": 10
            }
        },
        "required": []
    },
)

# Handler
async def get_trending_topics_handler(arguments: dict) -> list[types.TextContent]:
    """Get trending topics from recent news"""
    from collections import Counter
    import re
    
    days_back = arguments.get("days_back", 7)
    limit = arguments.get("limit", 10)
    
    try:
        # Get recent articles
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days_back)
        
        articles = news_collection.find({
            "published_date": {"$gte": cutoff}
        })
        
        # Extract words from titles and content
        words = []
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                    'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
                    'are', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did'}
        
        for article in articles:
            # Process title
            title_words = re.findall(r'\\b[a-z]{4,}\\b', article['title'].lower())
            words.extend([w for w in title_words if w not in stopwords])
            
            # Process content (first 200 chars)
            content = article['content'][:200]
            content_words = re.findall(r'\\b[a-z]{4,}\\b', content.lower())
            words.extend([w for w in content_words if w not in stopwords])
        
        # Count word frequency
        word_counts = Counter(words)
        trending = word_counts.most_common(limit)
        
        # Build response
        result = f"📈 **Trending Topics (Last {days_back} Days)**\\n\\n"
        
        for idx, (word, count) in enumerate(trending, 1):
            bar = "█" * min(count, 20)  # Visual bar
            result += f"{idx}. **{word.capitalize()}** - {count} mentions\\n"
            result += f"   {bar}\\n\\n"
        
        return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"Error getting trending topics: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error analyzing trending topics: {str(e)}"
        )]
```

---

## Example 5: RSS Feed Importer

Import news from RSS feeds.

### Add dependency to requirements.txt

```
feedparser>=6.0.10
```

### Implementation

```python
import feedparser

# In handle_list_tools()
types.Tool(
    name="import_rss_feed",
    description="Import news articles from an RSS feed URL",
    inputSchema={
        "type": "object",
        "properties": {
            "feed_url": {
                "type": "string",
                "description": "RSS feed URL to import from"
            },
            "category": {
                "type": "string",
                "description": "Category to assign to imported articles"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of articles to import (default: 10)",
                "default": 10
            }
        },
        "required": ["feed_url", "category"]
    },
)

# Handler
async def import_rss_feed_handler(arguments: dict) -> list[types.TextContent]:
    """Import news from an RSS feed"""
    feed_url = arguments.get("feed_url")
    category = arguments.get("category")
    limit = arguments.get("limit", 10)
    
    if not feed_url or not category:
        return [types.TextContent(
            type="text",
            text="Error: Please provide feed_url and category."
        )]
    
    try:
        # Parse RSS feed
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            return [types.TextContent(
                type="text",
                text=f"No articles found in feed: {feed_url}"
            )]
        
        # Import articles
        imported = 0
        for entry in feed.entries[:limit]:
            article = {
                "title": entry.get("title", "Untitled"),
                "content": entry.get("summary", entry.get("description", "")),
                "category": category,
                "source": feed.feed.get("title", "RSS Feed"),
                "url": entry.get("link", ""),
                "published_date": datetime.now()
            }
            
            # Check if article already exists
            existing = news_collection.find_one({
                "title": article["title"],
                "url": article["url"]
            })
            
            if not existing:
                news_collection.insert_one(article)
                imported += 1
        
        result = f"✅ **RSS Import Complete**\\n\\n"
        result += f"**Feed:** {feed.feed.get('title', feed_url)}\\n"
        result += f"**Category:** {category}\\n"
        result += f"**Found:** {len(feed.entries)} articles\\n"
        result += f"**Imported:** {imported} new articles\\n"
        result += f"**Skipped:** {len(feed.entries[:limit]) - imported} duplicates"
        
        return [types.TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"Error importing RSS feed: {e}")
        return [types.TextContent(
            type="text",
            text=f"Error importing RSS feed: {str(e)}"
        )]
```

---

## 🎯 Testing Your Tools

### 1. Update requirements.txt (if needed)

```bash
pip install -r requirements.txt
```

### 2. Restart the MCP server

```bash
python src/server.py
```

### 3. Test in ChatGPT

```
"Add a news article about Python programming"
"Get news database statistics"
"What are the trending topics from last 3 days?"
"Import news from https://example.com/rss"
```

---

## 💡 Best Practices

1. **Validate Inputs**: Always check required parameters
2. **Handle Errors**: Use try-except blocks
3. **Log Operations**: Use logger for debugging
4. **Return Formatted Text**: Use markdown for readability
5. **Check Duplicates**: Before inserting data
6. **Use Indexes**: For frequently queried fields
7. **Test Thoroughly**: Before deploying

---

## 🚀 Ideas for More Tools

- **Sentiment Analysis**: Analyze news sentiment
- **Summary Generator**: Create article summaries
- **Email Alerts**: Send news digests
- **Image Recognition**: Extract info from news images
- **Translation**: Translate articles to other languages
- **Bookmark System**: Let users save favorite articles
- **Comments**: Add commenting functionality
- **Share**: Share articles to social media
- **Export**: Export news to PDF/CSV

---

## 📚 Resources

- [MCP SDK Documentation](https://modelcontextprotocol.io/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)

---

## 🤝 Contributing

Have a cool tool idea? Contribute it!

1. Fork the repository
2. Create your feature branch
3. Add your tool following the examples
4. Test thoroughly
5. Submit a pull request

---

**Happy coding!** 🎉
