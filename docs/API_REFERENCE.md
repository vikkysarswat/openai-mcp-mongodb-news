# API Reference: MongoDB News MCP Server

## Overview

This document provides detailed API reference for the MongoDB News MCP Server tools.

## Tools

### 1. fetch_news

Fetch news articles from MongoDB with filtering and sorting options.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| category | string | No | null | Filter news by category (case-insensitive partial match) |
| limit | integer | No | 10 | Maximum number of articles to return (1-100) |
| sort_by | string | No | "date" | Sort order: "date" or "relevance" |
| days_back | integer | No | 7 | Fetch news from last N days |

#### Example Requests

```json
// Get latest 5 technology articles
{
  "category": "Technology",
  "limit": 5,
  "sort_by": "date",
  "days_back": 7
}

// Get all news from last 3 days
{
  "limit": 20,
  "days_back": 3
}

// Get business news
{
  "category": "Business",
  "limit": 10
}
```

#### Response Format

```
📰 **News Feed**

Found 5 article(s)

============================================================

**1. Article Title**
📂 Category: Technology
📰 Source: Tech News Daily
📅 Published: October 15, 2025 10:30 AM

Article content preview (first 200 characters)...

🔗 Read more: https://example.com/article

------------------------------------------------------------

**2. Second Article Title**
...
```

---

### 2. search_news

Search news articles by keywords in title or content.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | Yes | - | Search keywords to find in title or content |
| limit | integer | No | 10 | Maximum number of results to return (1-100) |

#### Example Requests

```json
// Search for AI-related articles
{
  "query": "artificial intelligence",
  "limit": 5
}

// Search for climate news
{
  "query": "climate change",
  "limit": 10
}

// Search for specific company
{
  "query": "Tesla"
}
```

#### Response Format

```
📰 **Search: artificial intelligence**

Found 3 article(s)

============================================================

**1. AI Breakthrough in Natural Language Processing**
📂 Category: Technology
📰 Source: Tech Journal
📅 Published: October 14, 2025 02:30 PM

Researchers have announced a significant breakthrough...

🔗 Read more: https://example.com/ai-breakthrough

------------------------------------------------------------
```

---

### 3. get_news_categories

Retrieve list of available news categories from the database.

#### Parameters

None

#### Example Request

```json
{}
```

#### Response Format

```
Available News Categories:

1. Technology
2. Business
3. Environment
4. Health
5. Sports
6. Entertainment
7. Science
8. History
```

---

## MongoDB Schema

### Collection: news

#### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| title | string | Article title |
| content | string | Article content/body |
| category | string | Article category |
| source | string | News source name |
| published_date | Date | Publication timestamp |

#### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| url | string | Article URL |
| author | string | Article author |
| image_url | string | Article image URL |
| tags | array | Article tags |

#### Indexes

```javascript
// Recommended indexes for performance
db.news.createIndex({ "category": 1 })
db.news.createIndex({ "published_date": -1 })
db.news.createIndex({ "title": "text", "content": "text" })
```

---

## Error Responses

### MongoDB Connection Error

```
Error: MongoDB connection not established. Please check your connection settings.
```

### No Results Found

```
No news articles found matching the criteria. Category: Technology, Days back: 7
```

### Search Query Missing

```
Please provide a search query.
```

### Database Error

```
Error fetching news from database: [error details]
```

---

## Response Formats

### Widget Display Format

News articles are formatted for optimal display in ChatGPT widgets:

1. **Header**: Category or search term with emoji
2. **Summary**: Number of articles found
3. **Article Cards**: Each article shows:
   - Title (bold)
   - Category with 📂 icon
   - Source with 📰 icon
   - Date with 📅 icon
   - Content preview (200 chars)
   - Read more link with 🔗 icon
4. **Separators**: Visual dividers between articles

---

## Rate Limits

No rate limits are currently enforced, but consider implementing:

- Max 100 results per query
- Recommended pagination for large result sets
- MongoDB query timeout: 5 seconds

---

## Best Practices

### For Developers

1. **Always use limit parameter** to prevent large result sets
2. **Index your MongoDB collections** for better performance
3. **Handle errors gracefully** with try-catch blocks
4. **Log important operations** for debugging
5. **Validate inputs** before database queries

### For Users

1. **Be specific with categories** for better filtering
2. **Use search for specific topics** rather than broad categories
3. **Adjust days_back** to find older or newer articles
4. **Start with small limits** and increase as needed

---

## Extensions

### Adding Custom Fields

To add custom fields to news articles:

1. Update MongoDB schema
2. Modify `format_news_for_widget()` in `server.py`
3. Update tool descriptions

### Creating New Tools

Example template for a new tool:

```python
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        # ... existing tools ...
        types.Tool(
            name="your_new_tool",
            description="What it does",
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
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    if name == "your_new_tool":
        return await your_new_tool_handler(arguments or {})
    # ... existing handlers ...

async def your_new_tool_handler(arguments: dict) -> list[types.TextContent]:
    # Implementation
    return [types.TextContent(type="text", text="Result")]
```

---

## Version History

### v1.0.0 (2025-10-15)
- Initial release
- fetch_news tool
- search_news tool
- get_news_categories tool
- MongoDB integration
- Widget display support

---

## Support

For questions or issues:
- GitHub Issues: [Report a bug](https://github.com/vikkysarswat/openai-mcp-mongodb-news/issues)
- Email: vikky.sarswat@gmail.com
