# OpenAI Apps SDK MongoDB News Connector

🚀 A **production-ready** OpenAI Apps SDK MCP server with MongoDB integration that displays news articles through **interactive widgets** in ChatGPT, following the official pizza example architecture.

## 🎯 What This Is

This is a **proper OpenAI Apps SDK implementation** that:
- ✅ Uses **FastMCP** (not stdio MCP)
- ✅ Implements **Streamable HTTP** transport
- ✅ Returns **widget metadata** (`_meta.openai/outputTemplate`)
- ✅ Serves **React-based UI components** as embedded resources
- ✅ Integrates with **MongoDB** for real data
- ✅ Follows the **pizza example** architecture from [openai/openai-apps-sdk-examples](https://github.com/openai/openai-apps-sdk-examples)

## 🏗️ Architecture

```
┌─────────────┐
│   ChatGPT   │  (OpenAI Apps SDK Client)
│  (Web/App)  │
└──────┬──────┘
       │ Streamable HTTP + SSE
       │ MCP Protocol
┌──────▼──────┐
│ MCP Server  │  (FastMCP - Python)
│   FastAPI   │  - Tools (fetch_news, search_news)
└──────┬──────┘  - Resources (widget HTML)
       │         - Metadata (_meta.openai/*)
┌──────▼──────┐
│  Widgets    │  (React Components)
│  (Browser)  │  - NewsListWidget
└─────────────┘  - NewsSearchWidget
       │
┌──────▼──────┐
│   MongoDB   │  (News Database)
└─────────────┘
```

## 📁 Project Structure

```
openai-mcp-mongodb-news/
├── server/                    # MCP Server (Python)
│   ├── main.py               # FastMCP server with widgets
│   └── requirements.txt      # Python dependencies
│
├── web/                      # Widget Components (React)
│   ├── src/
│   │   ├── NewsListWidget.tsx    # News feed widget
│   │   ├── NewsSearchWidget.tsx  # Search results widget
│   │   └── styles.css            # Widget styles
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── assets/                   # Built widget bundles
│   ├── news-list.js
│   ├── news-list.css
│   ├── news-search.js
│   └── news-search.css
│
├── scripts/                  # Setup scripts
│   └── setup_mongodb.py
│
└── docker-compose.yml        # Full stack deployment
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB 4.4+
- pnpm (recommended) or npm

### 1. Clone Repository

```bash
git clone https://github.com/vikkysarswat/openai-mcp-mongodb-news.git
cd openai-mcp-mongodb-news
```

### 2. Set Up MongoDB

```bash
# Option A: Local MongoDB
# Make sure MongoDB is running on localhost:27017

# Option B: Docker
docker-compose up -d mongodb

# Initialize with sample data
cd scripts
python -m venv .venv
source .venv/bin/activate
pip install pymongo python-dotenv
python setup_mongodb.py
```

### 3. Build Widgets

```bash
cd web
pnpm install  # or npm install
pnpm run build  # Builds to ../assets/
```

### 4. Run MCP Server

```bash
cd ../server
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# Set environment variables
export MONGODB_URI=\"mongodb://localhost:27017/\"
export MONGODB_DATABASE=\"news_db\"
export MONGODB_COLLECTION=\"news\"
export ASSET_BASE_URL=\"http://localhost:4444\"

# Start server
python main.py
```

Server will run on `http://localhost:8000`

### 5. Serve Widget Assets

```bash
# In another terminal
cd web
pnpm run serve  # Serves assets on http://localhost:4444
```

### 6. Expose with ngrok (for ChatGPT)

```bash
# In another terminal
ngrok http 8000
```

You'll get a URL like: `https://abc123.ngrok-free.app`

### 7. Connect to ChatGPT

1. Enable **Developer Mode** in ChatGPT Settings
2. Go to **Settings > Connectors**
3. Click **Add Connector**
4. Enter your ngrok URL: `https://abc123.ngrok-free.app/mcp`
5. The connector will auto-discover tools

## 🔧 Configuration

### Environment Variables

```bash
# MongoDB
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=news_db
MONGODB_COLLECTION=news

# Assets (where widgets are hosted)
ASSET_BASE_URL=http://localhost:4444

# For production
ASSET_BASE_URL=https://your-cdn.com
```

### Widget Asset Hosting

For **production**, host widget assets on a CDN:
- Upload `assets/*` to your CDN
- Update `ASSET_BASE_URL` in server
- Widgets load from CDN URLs

## 🛠️ Tools

### 1. fetch_news

Fetch news articles with filters.

```python
# ChatGPT usage
\"Show me technology news from the last 3 days\"

# Tool parameters
{
  \"category\": \"Technology\",  # Optional
  \"limit\": 10,              # Default: 10
  \"days_back\": 3            # Default: 7
}
```

**Returns:** News articles with interactive widget

### 2. search_news

Search news by keywords.

```python
# ChatGPT usage
\"Search for articles about artificial intelligence\"

# Tool parameters
{
  \"query\": \"artificial intelligence\",
  \"limit\": 10  # Default: 10
}
```

**Returns:** Search results with highlighted matches

### 3. get_news_categories

List available categories.

```python
# ChatGPT usage
\"What news categories are available?\"
```

**Returns:** List of categories with counts

## 🎨 Widgets

### NewsListWidget

Displays news articles in a card layout with:
- Article title, category badge, content preview
- Source and publication date
- \"Read More\" links to original articles
- Refresh button to reload
- Category filter (coming soon)

### NewsSearchWidget

Shows search results with:
- Search input for new queries
- Highlighted matching text
- Same card layout as NewsListWidget
- Search query display

### Widget Features

Both widgets use `window.openai` API:
- **window.openai.data** - Receives structured data
- **window.openai.callTool()** - Calls MCP tools
- **window.openai.sendFollowupMessage()** - Sends messages
- **window.openai.requestDisplayMode()** - Changes layout

## 📊 MongoDB Schema

```javascript
{
  \"_id\": ObjectId,
  \"title\": String,           // Required
  \"content\": String,         // Required
  \"category\": String,        // Required
  \"source\": String,          // Required
  \"published_date\": Date,    // Required
  \"url\": String,             // Optional
  \"author\": String,          // Optional
  \"image_url\": String        // Optional
}
```

## 🐳 Docker Deployment

```bash
# Full stack with Docker Compose
docker-compose up -d

# Server: http://localhost:8000/mcp
# Assets: http://localhost:4444
# MongoDB: localhost:27017
```

## 🧪 Testing

### 1. Test with MCP Inspector

```bash
# Install MCPJam or MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Connect to your server
mcp-inspector http://localhost:8000/mcp
```

### 2. Test Widgets Locally

```bash
cd web
pnpm run dev  # Opens Vite dev server
```

### 3. Test in ChatGPT

Enable Developer Mode and add connector

## 📚 Key Differences from Standard MCP

| Feature | Standard MCP | Apps SDK MCP |
|---------|-------------|--------------|
| Transport | stdio | HTTP/SSE |
| Tool Response | Text only | Text + Widget metadata |
| UI | None | React components |
| Metadata | Simple | `_meta.openai/*` required |
| Resources | Optional | Required for widgets |
| Client | Claude Desktop | ChatGPT Apps SDK |

## 🔗 Resources

- [OpenAI Apps SDK Examples](https://github.com/openai/openai-apps-sdk-examples)
- [Apps SDK Documentation](https://developers.openai.com/apps-sdk/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/)

## 🤝 Contributing

This follows OpenAI's Apps SDK architecture. When contributing:

1. Keep server logic in `server/main.py`
2. Keep widget UI in `web/src/`
3. Build widgets before testing
4. Follow React + TypeScript patterns
5. Use `window.openai` API for widget-server communication

## 📄 License

MIT License - see LICENSE file

## 👤 Author

**Nilesh Vikky**
- GitHub: [@vikkysarswat](https://github.com/vikkysarswat)
- Email: vikky.sarswat@gmail.com

---

⭐ **Star this repo** if you find it helpful!

🐛 **Report issues**: [GitHub Issues](https://github.com/vikkysarswat/openai-mcp-mongodb-news/issues)

💬 **Discussions**: [GitHub Discussions](https://github.com/vikkysarswat/openai-mcp-mongodb-news/discussions)
