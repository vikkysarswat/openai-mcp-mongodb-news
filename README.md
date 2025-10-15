# OpenAI MCP MongoDB News App

🚀 A Python-based Model Context Protocol (MCP) server that connects to ChatGPT, integrates with MongoDB, and displays news articles through interactive widgets.

## 📋 Overview

This project demonstrates how to build a ChatGPT connector using the MCP SDK that:
- Connects to MongoDB to fetch news articles
- Implements multiple tools (fetch_news, search_news, get_categories)
- Displays results as interactive widgets in ChatGPT (similar to the pizza example)
- Provides a foundation for building additional custom tools

## 🏗️ Architecture

```
┌─────────────┐
│   ChatGPT   │
│  (OpenAI)   │
└──────┬──────┘
       │ MCP Protocol
       │
┌──────▼──────┐
│ MCP Server  │
│  (Python)   │
└──────┬──────┘
       │
┌──────▼──────┐
│  MongoDB    │
│ (News Data) │
└─────────────┘
```

## 🛠️ Features

### Current Tools

1. **fetch_news** - Fetch news articles with filtering
   - Filter by category
   - Limit number of results
   - Sort by date or relevance
   - Filter by date range (days back)

2. **search_news** - Search news by keywords
   - Search in title and content
   - Limit results
   - Sort by relevance

3. **get_news_categories** - List all available categories

### Widget Display

News is formatted for widget display in ChatGPT, showing:
- Article title and preview
- Category, source, and publication date
- Read more links
- Rich formatting with emojis and structure

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- MongoDB 4.4 or higher
- OpenAI ChatGPT account with connector access

### Step 1: Clone the Repository

```bash
git clone https://github.com/vikkysarswat/openai-mcp-mongodb-news.git
cd openai-mcp-mongodb-news
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure MongoDB

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your MongoDB settings:
```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=news_db
MONGODB_COLLECTION=news
```

3. Set up the database with sample data:
```bash
python scripts/setup_mongodb.py
```

### Step 4: Configure ChatGPT Connector

1. Open the ChatGPT connector settings in your OpenAI account
2. Create a new connector using the configuration in `config/chatgpt_connector.json`
3. Update the environment variables in the connector settings

## 🚀 Running the Server

### Local Development

```bash
python src/server.py
```

### With Environment Variables

```bash
export MONGODB_URI="mongodb://localhost:27017/"
export MONGODB_DATABASE="news_db"
export MONGODB_COLLECTION="news"
python src/server.py
```

## 📖 Usage Examples

### In ChatGPT

Once connected, you can use natural language to interact with your news database:

```
"Show me the latest technology news"
"Search for articles about AI"
"What news categories are available?"
"Get news from the last 3 days"
"Show me business news from yesterday"
```

### Tool Parameters

#### fetch_news
```json
{
  "category": "Technology",
  "limit": 5,
  "sort_by": "date",
  "days_back": 7
}
```

#### search_news
```json
{
  "query": "artificial intelligence",
  "limit": 10
}
```

## 🗄️ MongoDB Schema

### News Collection

```javascript
{
  "_id": ObjectId,
  "title": String,
  "content": String,
  "category": String,
  "source": String,
  "url": String,
  "published_date": Date,
  "author": String (optional),
  "image_url": String (optional)
}
```

### Example Document

```json
{
  "title": "AI Breakthrough in Natural Language Processing",
  "content": "Researchers have announced a significant breakthrough...",
  "category": "Technology",
  "source": "Tech News Daily",
  "url": "https://example.com/article",
  "published_date": "2025-10-15T10:30:00Z"
}
```

## 🔧 Adding New Tools

To add a new tool to your MCP server:

1. **Define the tool** in `handle_list_tools()`:

```python
types.Tool(
    name="your_tool_name",
    description="What your tool does",
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

2. **Implement the handler** in `handle_call_tool()`:

```python
elif name == "your_tool_name":
    return await your_tool_handler(arguments or {})
```

3. **Create the handler function**:

```python
async def your_tool_handler(arguments: dict) -> list[types.TextContent]:
    # Your implementation here
    return [types.TextContent(type="text", text="Result")]
```

4. **Update the connector config** in `config/chatgpt_connector.json`

## 📝 Configuration Files

### chatgpt_connector.json

Defines the connector configuration for ChatGPT:
- Server name and description
- Command to run the MCP server
- Environment variables
- Tool definitions with widget settings

### .env

Environment variables for the server:
- MongoDB connection settings
- Server configuration
- Optional API keys

## 🐛 Troubleshooting

### MongoDB Connection Issues

```bash
# Check if MongoDB is running
mongosh

# Verify connection string
echo $MONGODB_URI
```

### MCP Server Issues

```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
python src/server.py
```

### ChatGPT Connector Issues

1. Verify the connector is properly configured
2. Check environment variables are set
3. Ensure the server is running and accessible
4. Review ChatGPT connector logs

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [OpenAI ChatGPT Connectors](https://platform.openai.com/docs/guides/connectors)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)

## 🤝 Contributing

Contributions are welcome! Here are some ideas for additional tools:

- `add_news` - Add news articles to the database
- `update_news` - Update existing news articles
- `delete_news` - Remove news articles
- `get_trending_topics` - Analyze trending topics
- `sentiment_analysis` - Analyze news sentiment
- `news_summary` - Generate summaries of multiple articles

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Nilesh Vikky**
- GitHub: [@vikkysarswat](https://github.com/vikkysarswat)
- Email: vikky.sarswat@gmail.com

## 🙏 Acknowledgments

- OpenAI for the MCP SDK and ChatGPT platform
- MongoDB for the excellent Python driver
- The open-source community for inspiration

## 📈 Roadmap

- [ ] Add authentication support
- [ ] Implement news caching
- [ ] Add image support in widgets
- [ ] Create web dashboard for news management
- [ ] Add RSS feed integration
- [ ] Implement real-time news updates
- [ ] Add multi-language support
- [ ] Create automated news scraping

---

⭐ If you find this project helpful, please give it a star!

🐛 Found a bug? [Open an issue](https://github.com/vikkysarswat/openai-mcp-mongodb-news/issues)

💡 Have a feature idea? [Start a discussion](https://github.com/vikkysarswat/openai-mcp-mongodb-news/discussions)
