FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MONGODB_URI=mongodb://host.docker.internal:27017/
ENV MONGODB_DATABASE=news_db
ENV MONGODB_COLLECTION=news

# Run the MCP server
CMD ["python", "src/server.py"]
