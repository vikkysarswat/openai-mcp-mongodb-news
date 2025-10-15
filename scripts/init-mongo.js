// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

db = db.getSiblingDB('news_db');

print('Creating news_db database...');

// Create collection
db.createCollection('news');

print('Creating indexes...');

// Create indexes for better query performance
db.news.createIndex({ "category": 1 });
db.news.createIndex({ "published_date": -1 });
db.news.createIndex({ "title": "text", "content": "text" });

print('Inserting sample news data...');

// Insert sample news articles
db.news.insertMany([
  {
    title: "AI Breakthrough: New Model Achieves Human-Level Performance",
    content: "Researchers have announced a significant breakthrough in artificial intelligence, with a new model demonstrating human-level performance across multiple benchmarks. The model shows unprecedented capabilities in reasoning, understanding context, and generating creative solutions.",
    category: "Technology",
    source: "Tech News Daily",
    url: "https://example.com/ai-breakthrough",
    published_date: new Date(Date.now() - 2*60*60*1000) // 2 hours ago
  },
  {
    title: "Global Markets Rally on Positive Economic Data",
    content: "Stock markets worldwide experienced significant gains today following the release of encouraging economic indicators. Investors responded enthusiastically to reports showing stronger-than-expected job growth and declining inflation rates.",
    category: "Business",
    source: "Financial Times",
    url: "https://example.com/markets-rally",
    published_date: new Date(Date.now() - 5*60*60*1000) // 5 hours ago
  },
  {
    title: "Climate Summit Reaches Historic Agreement",
    content: "World leaders have signed a groundbreaking climate agreement at this year's international summit. The accord includes concrete commitments to reduce carbon emissions and transition to renewable energy sources over the next decade.",
    category: "Environment",
    source: "World News Network",
    url: "https://example.com/climate-summit",
    published_date: new Date(Date.now() - 24*60*60*1000) // 1 day ago
  },
  {
    title: "New Study Reveals Benefits of Mediterranean Diet",
    content: "A comprehensive 10-year study has provided compelling evidence for the health benefits of the Mediterranean diet. Researchers found significant reductions in heart disease, diabetes, and cognitive decline among participants who followed the diet.",
    category: "Health",
    source: "Health Journal",
    url: "https://example.com/mediterranean-diet",
    published_date: new Date(Date.now() - 2*24*60*60*1000) // 2 days ago
  },
  {
    title: "Championship Team Secures Victory in Overtime",
    content: "In a thrilling overtime finish, the home team secured their championship victory with a dramatic last-minute goal. The match, which kept fans on the edge of their seats, will be remembered as one of the most exciting games of the season.",
    category: "Sports",
    source: "Sports Daily",
    url: "https://example.com/championship-victory",
    published_date: new Date(Date.now() - 32*60*60*1000) // ~1.3 days ago
  },
  {
    title: "Streaming Platform Announces Record-Breaking Series",
    content: "The latest series from a major streaming platform has shattered viewing records, becoming the most-watched premiere in the platform's history. The show has captivated audiences worldwide with its compelling storyline and stellar cast.",
    category: "Entertainment",
    source: "Entertainment Weekly",
    url: "https://example.com/streaming-record",
    published_date: new Date(Date.now() - 12*60*60*1000) // 12 hours ago
  },
  {
    title: "Scientists Discover New Species in Deep Ocean",
    content: "Marine biologists have discovered several previously unknown species during a deep-sea expedition. The findings include unique bioluminescent creatures that thrive in extreme pressure conditions thousands of meters below the surface.",
    category: "Science",
    source: "Science Today",
    url: "https://example.com/ocean-discovery",
    published_date: new Date(Date.now() - 3*24*60*60*1000) // 3 days ago
  },
  {
    title: "Tech Giant Unveils Revolutionary Quantum Computer",
    content: "A leading technology company has unveiled its latest quantum computer, claiming it can solve complex problems exponentially faster than traditional supercomputers. The breakthrough could revolutionize fields from cryptography to drug discovery.",
    category: "Technology",
    source: "Tech News Daily",
    url: "https://example.com/quantum-computer",
    published_date: new Date(Date.now() - 2.5*24*60*60*1000) // ~2.5 days ago
  },
  {
    title: "Renewable Energy Surpasses Fossil Fuels in Power Generation",
    content: "For the first time in history, renewable energy sources have generated more electricity than fossil fuels in several major economies. This milestone represents a significant step toward global sustainability goals.",
    category: "Environment",
    source: "Green Energy News",
    url: "https://example.com/renewable-milestone",
    published_date: new Date(Date.now() - 4*24*60*60*1000) // 4 days ago
  },
  {
    title: "Archaeological Team Uncovers Ancient Civilization Artifacts",
    content: "Archaeologists working in a remote region have discovered artifacts from a previously unknown ancient civilization. The findings include intricate pottery, tools, and evidence of advanced agricultural practices dating back over 5,000 years.",
    category: "History",
    source: "Archaeology Monthly",
    url: "https://example.com/ancient-discovery",
    published_date: new Date(Date.now() - 5*24*60*60*1000) // 5 days ago
  }
]);

print('Database initialization complete!');
print('Total documents inserted: ' + db.news.count());
