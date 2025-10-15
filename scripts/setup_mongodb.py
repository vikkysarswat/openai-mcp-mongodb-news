#!/usr/bin/env python3
"""
Script to set up MongoDB with sample news data
"""

import os
from datetime import datetime, timedelta
import random
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Sample news data
SAMPLE_NEWS = [
    {
        "title": "AI Breakthrough: New Model Achieves Human-Level Performance",
        "content": "Researchers have announced a significant breakthrough in artificial intelligence, with a new model demonstrating human-level performance across multiple benchmarks. The model shows unprecedented capabilities in reasoning, understanding context, and generating creative solutions.",
        "category": "Technology",
        "source": "Tech News Daily",
        "url": "https://example.com/ai-breakthrough",
        "published_date": datetime.now() - timedelta(hours=2)
    },
    {
        "title": "Global Markets Rally on Positive Economic Data",
        "content": "Stock markets worldwide experienced significant gains today following the release of encouraging economic indicators. Investors responded enthusiastically to reports showing stronger-than-expected job growth and declining inflation rates.",
        "category": "Business",
        "source": "Financial Times",
        "url": "https://example.com/markets-rally",
        "published_date": datetime.now() - timedelta(hours=5)
    },
    {
        "title": "Climate Summit Reaches Historic Agreement",
        "content": "World leaders have signed a groundbreaking climate agreement at this year's international summit. The accord includes concrete commitments to reduce carbon emissions and transition to renewable energy sources over the next decade.",
        "category": "Environment",
        "source": "World News Network",
        "url": "https://example.com/climate-summit",
        "published_date": datetime.now() - timedelta(days=1)
    },
    {
        "title": "New Study Reveals Benefits of Mediterranean Diet",
        "content": "A comprehensive 10-year study has provided compelling evidence for the health benefits of the Mediterranean diet. Researchers found significant reductions in heart disease, diabetes, and cognitive decline among participants who followed the diet.",
        "category": "Health",
        "source": "Health Journal",
        "url": "https://example.com/mediterranean-diet",
        "published_date": datetime.now() - timedelta(days=2)
    },
    {
        "title": "Championship Team Secures Victory in Overtime",
        "content": "In a thrilling overtime finish, the home team secured their championship victory with a dramatic last-minute goal. The match, which kept fans on the edge of their seats, will be remembered as one of the most exciting games of the season.",
        "category": "Sports",
        "source": "Sports Daily",
        "url": "https://example.com/championship-victory",
        "published_date": datetime.now() - timedelta(days=1, hours=8)
    },
    {
        "title": "Streaming Platform Announces Record-Breaking Series",
        "content": "The latest series from a major streaming platform has shattered viewing records, becoming the most-watched premiere in the platform's history. The show has captivated audiences worldwide with its compelling storyline and stellar cast.",
        "category": "Entertainment",
        "source": "Entertainment Weekly",
        "url": "https://example.com/streaming-record",
        "published_date": datetime.now() - timedelta(hours=12)
    },
    {
        "title": "Scientists Discover New Species in Deep Ocean",
        "content": "Marine biologists have discovered several previously unknown species during a deep-sea expedition. The findings include unique bioluminescent creatures that thrive in extreme pressure conditions thousands of meters below the surface.",
        "category": "Science",
        "source": "Science Today",
        "url": "https://example.com/ocean-discovery",
        "published_date": datetime.now() - timedelta(days=3)
    },
    {
        "title": "Tech Giant Unveils Revolutionary Quantum Computer",
        "content": "A leading technology company has unveiled its latest quantum computer, claiming it can solve complex problems exponentially faster than traditional supercomputers. The breakthrough could revolutionize fields from cryptography to drug discovery.",
        "category": "Technology",
        "source": "Tech News Daily",
        "url": "https://example.com/quantum-computer",
        "published_date": datetime.now() - timedelta(days=2, hours=6)
    },
    {
        "title": "Renewable Energy Surpasses Fossil Fuels in Power Generation",
        "content": "For the first time in history, renewable energy sources have generated more electricity than fossil fuels in several major economies. This milestone represents a significant step toward global sustainability goals.",
        "category": "Environment",
        "source": "Green Energy News",
        "url": "https://example.com/renewable-milestone",
        "published_date": datetime.now() - timedelta(days=4)
    },
    {
        "title": "Archaeological Team Uncovers Ancient Civilization Artifacts",
        "content": "Archaeologists working in a remote region have discovered artifacts from a previously unknown ancient civilization. The findings include intricate pottery, tools, and evidence of advanced agricultural practices dating back over 5,000 years.",
        "category": "History",
        "source": "Archaeology Monthly",
        "url": "https://example.com/ancient-discovery",
        "published_date": datetime.now() - timedelta(days=5)
    }
]


def setup_database():
    """Set up MongoDB with sample news data"""
    try:
        # Connect to MongoDB
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        db_name = os.getenv("MONGODB_DATABASE", "news_db")
        collection_name = os.getenv("MONGODB_COLLECTION", "news")
        
        print(f"Connecting to MongoDB at {mongo_uri}...")
        client = MongoClient(mongo_uri)
        
        # Test connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        
        # Get database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        # Clear existing data
        print(f"Clearing existing data from {collection_name}...")
        collection.delete_many({})
        
        # Insert sample data
        print(f"Inserting {len(SAMPLE_NEWS)} sample news articles...")
        result = collection.insert_many(SAMPLE_NEWS)
        print(f"Successfully inserted {len(result.inserted_ids)} articles!")
        
        # Create indexes for better performance
        print("Creating indexes...")
        collection.create_index("category")
        collection.create_index("published_date")
        collection.create_index([("title", "text"), ("content", "text")])
        print("Indexes created successfully!")
        
        # Display summary
        print("\n" + "="*60)
        print("Database Setup Complete!")
        print("="*60)
        print(f"Database: {db_name}")
        print(f"Collection: {collection_name}")
        print(f"Total articles: {collection.count_documents({})}")
        
        # Show categories
        categories = collection.distinct("category")
        print(f"\nCategories: {', '.join(categories)}")
        
        print("\nYou can now run the MCP server with: python src/server.py")
        
        client.close()
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False
    
    return True


if __name__ == "__main__":
    setup_database()
