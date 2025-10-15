# 🚀 Quick Start Guide

Get your MongoDB News MCP server running in 5 minutes!

## ⚡ Option 1: Local Setup (Fastest)

### Prerequisites
- Python 3.10+
- MongoDB running locally

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/vikkysarswat/openai-mcp-mongodb-news.git
cd openai-mcp-mongodb-news

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env

# 5. Initialize database with sample data
python scripts/setup_mongodb.py

# 6. Run the server
python src/server.py
```

**That's it!** Your MCP server is now running and ready to connect to ChatGPT.

---

## 🐳 Option 2: Docker Setup (Easiest)

### Prerequisites
- Docker and Docker Compose

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/vikkysarswat/openai-mcp-mongodb-news.git
cd openai-mcp-mongodb-news

# 2. Start everything with Docker Compose
docker-compose up -d

# 3. Check if it's running
docker-compose ps
```

**Done!** MongoDB and MCP server are running in containers.

---

## 🔗 Connect to ChatGPT

### For OpenAI ChatGPT

1. Open ChatGPT Settings
2. Go to **Integrations** or **Connectors**
3. Click **Add Custom Connector**
4. Use the configuration from `config/chatgpt_connector.json`
5. Set your MongoDB connection details
6. Save and enable the connector

### For Claude Desktop

Edit your Claude config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add:
```json
{
  "mcpServers": {
    "mongodb-news": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "MONGODB_URI": "mongodb://localhost:27017/",
        "MONGODB_DATABASE": "news_db",
        "MONGODB_COLLECTION": "news"
      },
      "cwd": "/path/to/openai-mcp-mongodb-news"
    }
  }
}
```

---

## 🧪 Test Your Setup

Once connected, try these queries in ChatGPT:

```
"Show me the latest technology news"
"Search for articles about AI"
"What news categories are available?"
"Get business news from the last 3 days"
```

---

## 📊 Database Overview

Your MongoDB now has:
- **Database:** `news_db`
- **Collection:** `news`
- **10 sample articles** across 8 categories
- **Indexed fields** for fast queries

### View Your Data

```bash
mongosh
use news_db
db.news.find().pretty()
```

---

## 🎯 Next Steps

### 1. Add Your Own News
```python
# Edit scripts/setup_mongodb.py and add your articles
```

### 2. Create New Tools
See `docs/API_REFERENCE.md` for examples

### 3. Customize Widget Display
Edit `format_news_for_widget()` in `src/server.py`

### 4. Connect to Real News APIs
- NewsAPI
- RSS Feeds
- Web scraping

---

## 🐛 Common Issues

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
mongosh

# Or restart MongoDB
# macOS/Linux:
sudo systemctl restart mongod
# Docker:
docker-compose restart mongodb
```

### Port Already in Use
```bash
# Check what's using port 27017
lsof -i :27017  # macOS/Linux
netstat -ano | findstr :27017  # Windows

# Kill the process or use a different port
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Documentation

- **[README.md](README.md)** - Full project overview
- **[docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Detailed setup instructions
- **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - API documentation
- **[docs/WIDGET_EXAMPLES.md](docs/WIDGET_EXAMPLES.md)** - Widget display examples

---

## 💡 Tips

- Start with the sample data to understand the structure
- Use the widget examples to see how results are formatted
- Check the API reference when creating new tools
- Join the discussions for help and ideas

---

## 🤝 Need Help?

- 📖 Read the [full documentation](README.md)
- 🐛 [Report issues](https://github.com/vikkysarswat/openai-mcp-mongodb-news/issues)
- 💬 [Start a discussion](https://github.com/vikkysarswat/openai-mcp-mongodb-news/discussions)
- 📧 Email: vikky.sarswat@gmail.com

---

## ⭐ What's Next?

Now that you have the basic setup running, explore these features:

1. **Fetch News** - Get latest articles by category
2. **Search News** - Find articles by keywords
3. **Categories** - List available news categories
4. **Add Your Tools** - Build custom functionality

Happy coding! 🎉
