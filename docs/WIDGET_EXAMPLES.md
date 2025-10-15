# Widget Display Examples

This document shows examples of how news will be displayed in ChatGPT widgets.

## Example 1: Fetch Technology News

### User Query
```
"Show me the latest technology news"
```

### Widget Display
```
📰 **Technology**

Found 3 article(s)

============================================================

**1. AI Breakthrough: New Model Achieves Human-Level Performance**
📂 Category: Technology
📰 Source: Tech News Daily
📅 Published: October 15, 2025 08:30 AM

Researchers have announced a significant breakthrough in artificial intelligence, with a new model demonstrating human-level performance across multiple benchmarks. The model shows unprecedented...

🔗 Read more: https://example.com/ai-breakthrough

------------------------------------------------------------

**2. Tech Giant Unveils Revolutionary Quantum Computer**
📂 Category: Technology
📰 Source: Tech News Daily
📅 Published: October 13, 2025 06:30 AM

A leading technology company has unveiled its latest quantum computer, claiming it can solve complex problems exponentially faster than traditional supercomputers. The breakthrough could revoluti...

🔗 Read more: https://example.com/quantum-computer

------------------------------------------------------------
```

---

## Example 2: Search News

### User Query
```
"Search for articles about climate"
```

### Widget Display
```
📰 **Search: climate**

Found 2 article(s)

============================================================

**1. Climate Summit Reaches Historic Agreement**
📂 Category: Environment
📰 Source: World News Network
📅 Published: October 14, 2025 10:30 AM

World leaders have signed a groundbreaking climate agreement at this year's international summit. The accord includes concrete commitments to reduce carbon emissions and transition to renewable...

🔗 Read more: https://example.com/climate-summit

------------------------------------------------------------

**2. Renewable Energy Surpasses Fossil Fuels in Power Generation**
📂 Category: Environment
📰 Source: Green Energy News
📅 Published: October 11, 2025 10:30 AM

For the first time in history, renewable energy sources have generated more electricity than fossil fuels in several major economies. This milestone represents a significant step toward global...

🔗 Read more: https://example.com/renewable-milestone

------------------------------------------------------------
```

---

## Example 3: Get All Categories

### User Query
```
"What news categories are available?"
```

### Widget Display
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

## Example 4: Recent News (All Categories)

### User Query
```
"Show me news from the last 24 hours"
```

### Widget Display
```
📰 **News Feed**

Found 5 article(s)

============================================================

**1. AI Breakthrough: New Model Achieves Human-Level Performance**
📂 Category: Technology
📰 Source: Tech News Daily
📅 Published: October 15, 2025 08:30 AM

Researchers have announced a significant breakthrough in artificial intelligence...

🔗 Read more: https://example.com/ai-breakthrough

------------------------------------------------------------

**2. Streaming Platform Announces Record-Breaking Series**
📂 Category: Entertainment
📰 Source: Entertainment Weekly
📅 Published: October 14, 2025 10:30 PM

The latest series from a major streaming platform has shattered viewing records...

🔗 Read more: https://example.com/streaming-record

------------------------------------------------------------

**3. Global Markets Rally on Positive Economic Data**
📂 Category: Business
📰 Source: Financial Times
📅 Published: October 14, 2025 05:30 PM

Stock markets worldwide experienced significant gains today following the release...

🔗 Read more: https://example.com/markets-rally

------------------------------------------------------------

**4. Climate Summit Reaches Historic Agreement**
📂 Category: Environment
📰 Source: World News Network
📅 Published: October 14, 2025 10:30 AM

World leaders have signed a groundbreaking climate agreement at this year's...

🔗 Read more: https://example.com/climate-summit

------------------------------------------------------------

**5. Championship Team Secures Victory in Overtime**
📂 Category: Sports
📰 Source: Sports Daily
📅 Published: October 14, 2025 02:30 AM

In a thrilling overtime finish, the home team secured their championship victory...

🔗 Read more: https://example.com/championship-victory

------------------------------------------------------------
```

---

## Example 5: Limited Results

### User Query
```
"Show me 2 health articles"
```

### Widget Display
```
📰 **Health**

Found 2 article(s)

============================================================

**1. New Study Reveals Benefits of Mediterranean Diet**
📂 Category: Health
📰 Source: Health Journal
📅 Published: October 13, 2025 10:30 AM

A comprehensive 10-year study has provided compelling evidence for the health benefits of the Mediterranean diet. Researchers found significant reductions in heart disease, diabetes, and cognitiv...

🔗 Read more: https://example.com/mediterranean-diet

------------------------------------------------------------
```

---

## Example 6: No Results

### User Query
```
"Show me news about cryptocurrency"
```

### Widget Display
```
No news articles found matching the criteria. Category: cryptocurrency, Days back: 7
```

---

## Widget Features

### Visual Elements
- 📰 News/Article icon
- 📂 Category icon
- 📅 Date/Time icon
- 🔗 Link icon
- **Bold titles** for emphasis
- Clear separators between articles

### Information Hierarchy
1. **Category/Search term** (Header)
2. **Article count** (Summary)
3. **Article details** (Cards):
   - Title (most prominent)
   - Metadata (category, source, date)
   - Content preview
   - Action link

### Design Principles
- **Scannable**: Users can quickly browse titles
- **Informative**: Key metadata visible at a glance
- **Actionable**: Direct links to full articles
- **Consistent**: Same format across all results
- **Accessible**: Clear structure with icons and formatting

---

## Customization Options

You can customize the widget display by modifying the `format_news_for_widget()` function in `src/server.py`:

### Add Image Support
```python
if article.get("image_url"):
    result += f"![Article Image]({article['image_url']})\n\n"
```

### Add Author Information
```python
author = article.get("author", "Unknown")
result += f"✍️ Author: {author}\n"
```

### Add Tags
```python
tags = article.get("tags", [])
if tags:
    result += f"🏷️ Tags: {', '.join(tags)}\n"
```

### Adjust Content Preview Length
```python
# Change from 200 to 300 characters
content_preview = content[:300] + "..." if len(content) > 300 else content
```

---

## Integration with ChatGPT

When using this MCP server with ChatGPT:

1. **Natural Language**: Users can use conversational queries
2. **Automatic Tool Selection**: ChatGPT chooses the right tool
3. **Parameter Inference**: ChatGPT extracts parameters from queries
4. **Rich Display**: Results shown in formatted widgets
5. **Follow-up Questions**: Users can refine searches interactively

### Example Conversation Flow

```
User: "Show me technology news"
ChatGPT: [Calls fetch_news with category="Technology"]
         [Displays widget with results]

User: "Now search for AI articles"
ChatGPT: [Calls search_news with query="AI"]
         [Displays refined results]

User: "What other categories do you have?"
ChatGPT: [Calls get_news_categories]
         [Displays category list]

User: "Show me sports news from yesterday"
ChatGPT: [Calls fetch_news with category="Sports", days_back=1]
         [Displays filtered results]
```

---

## Best Practices

### For Content Display
- Keep titles concise and descriptive
- Use consistent date formatting
- Include source attribution
- Provide clear call-to-action links
- Truncate long content appropriately

### For User Experience
- Show article count upfront
- Use visual separators
- Maintain consistent spacing
- Include relevant metadata
- Make links easily identifiable

### For Performance
- Limit default results to 10
- Cache frequently requested categories
- Use database indexes
- Optimize query patterns
- Handle errors gracefully
