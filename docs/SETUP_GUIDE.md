# Setup Guide: MongoDB News MCP Server

## Complete Step-by-Step Setup

### 1. System Requirements

#### Software Requirements
- **Python**: 3.10 or higher
- **MongoDB**: 4.4 or higher
- **pip**: Latest version
- **Git**: For cloning the repository

#### Platform Support
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian, CentOS)

### 2. Installing MongoDB

#### On macOS (using Homebrew)
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### On Ubuntu/Debian
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### On Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run the installer
3. Choose "Complete" installation
4. Install MongoDB as a service
5. Verify installation: `mongod --version`

#### Using Docker
```bash
docker run -d -p 27017:27017 --name mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:latest
```

### 3. Setting Up the Project

#### Clone and Install
```bash
# Clone repository
git clone https://github.com/vikkysarswat/openai-mcp-mongodb-news.git
cd openai-mcp-mongodb-news

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuring Environment

#### Create .env file
```bash
cp .env.example .env
```

#### Edit .env with your settings

**For local MongoDB:**
```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=news_db
MONGODB_COLLECTION=news
SERVER_NAME=mongodb-news-mcp
SERVER_VERSION=1.0.0
```

**For MongoDB Atlas (cloud):**
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=news_db
MONGODB_COLLECTION=news
SERVER_NAME=mongodb-news-mcp
SERVER_VERSION=1.0.0
```

**For Docker:**
```env
MONGODB_URI=mongodb://admin:password@localhost:27017/
MONGODB_DATABASE=news_db
MONGODB_COLLECTION=news
SERVER_NAME=mongodb-news-mcp
SERVER_VERSION=1.0.0
```

### 5. Initialize Database

```bash
# Run the setup script
python scripts/setup_mongodb.py
```

**Expected output:**
```
Connecting to MongoDB at mongodb://localhost:27017/...
Successfully connected to MongoDB!
Clearing existing data from news...
Inserting 10 sample news articles...
Successfully inserted 10 articles!
Creating indexes...
Indexes created successfully!

============================================================
Database Setup Complete!
============================================================
Database: news_db
Collection: news
Total articles: 10

Categories: Technology, Business, Environment, Health, Sports, Entertainment, Science, History

You can now run the MCP server with: python src/server.py
```

### 6. Testing the Server

#### Start the server
```bash
python src/server.py
```

**Expected output:**
```
INFO:__main__:Starting MongoDB News MCP Server...
INFO:__main__:Connecting to MongoDB at mongodb://localhost:27017/
INFO:__main__:Successfully connected to MongoDB
INFO:__main__:MCP Server is running...
```

### 7. Setting Up ChatGPT Connector

#### Option 1: Using ChatGPT Desktop/Web App

1. Open ChatGPT Settings
2. Navigate to "Integrations" or "Connectors"
3. Click "Add Custom Connector"
4. Upload or paste the content from `config/chatgpt_connector.json`
5. Configure environment variables:
   - MONGODB_URI
   - MONGODB_DATABASE
   - MONGODB_COLLECTION
6. Save and enable the connector

#### Option 2: Using Claude Desktop MCP Configuration

Edit your Claude desktop config file:

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

### 8. Verification

#### Test MongoDB Connection
```bash
mongosh
use news_db
db.news.countDocuments()
# Should return 10
```

#### Test MCP Server
In ChatGPT or Claude, try:
- "Show me the latest news"
- "What are the available news categories?"
- "Search for technology news"

### 9. Troubleshooting

#### MongoDB Connection Failed
```bash
# Check MongoDB status
# macOS/Linux:
sudo systemctl status mongod
# or
mongosh

# Windows:
sc query MongoDB
```

#### Port Already in Use
```bash
# Find process using port 27017
# macOS/Linux:
lsof -i :27017
# Windows:
netstat -ano | findstr :27017

# Kill the process or use a different port
```

#### Python Dependencies Issues
```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install -r requirements.txt --no-cache-dir

# If pymongo fails
pip install pymongo --force-reinstall
```

#### MCP Server Not Responding
```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
python src/server.py

# Check for port conflicts
# The MCP server uses stdio, not network ports
```

### 10. Production Deployment

#### Using systemd (Linux)

Create `/etc/systemd/system/mcp-news.service`:
```ini
[Unit]
Description=MongoDB News MCP Server
After=network.target mongodb.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/openai-mcp-mongodb-news
Environment="MONGODB_URI=mongodb://localhost:27017/"
Environment="MONGODB_DATABASE=news_db"
Environment="MONGODB_COLLECTION=news"
ExecStart=/path/to/venv/bin/python src/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mcp-news
sudo systemctl start mcp-news
sudo systemctl status mcp-news
```

#### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/server.py"]
```

Build and run:
```bash
docker build -t mcp-news-server .
docker run -d \
  -e MONGODB_URI="mongodb://host.docker.internal:27017/" \
  -e MONGODB_DATABASE="news_db" \
  -e MONGODB_COLLECTION="news" \
  --name mcp-news \
  mcp-news-server
```

### 11. Security Best Practices

1. **Never commit .env file**
2. **Use strong MongoDB passwords**
3. **Enable MongoDB authentication**
4. **Use TLS/SSL for MongoDB connections**
5. **Restrict MongoDB network access**
6. **Keep dependencies updated**
7. **Use environment variables for secrets**

### 12. Next Steps

- Add custom news sources
- Implement additional tools
- Set up automated news scraping
- Add authentication
- Create a web dashboard
- Set up monitoring and logging

### 13. Getting Help

- **Issues**: [GitHub Issues](https://github.com/vikkysarswat/openai-mcp-mongodb-news/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vikkysarswat/openai-mcp-mongodb-news/discussions)
- **Email**: vikky.sarswat@gmail.com

---

**Setup Complete!** 🎉

You now have a fully functional MCP server that can:
- Fetch news from MongoDB
- Display results in ChatGPT widgets
- Search and filter news articles
- Serve as a foundation for additional tools
