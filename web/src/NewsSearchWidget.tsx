import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

interface Article {
  _id: string;
  title: string;
  content: string;
  category: string;
  source: string;
  url?: string;
  published_date: string;
}

interface SearchData {
  articles: Article[];
  query: string;
  count: number;
}

function NewsSearchWidget() {
  const [data, setData] = useState<SearchData | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        if (window.openai?.data) {
          const searchData = window.openai.data as SearchData;
          setData(searchData);
          setSearchQuery(searchData.query);
        }
      } catch (error) {
        console.error('Error loading search data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();

    window.openai?.onData?.((newData: SearchData) => {
      setData(newData);
      setSearchQuery(newData.query);
    });
  }, []);

  const handleSearch = async (query: string) => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      await window.openai?.callTool('search_news', {
        query: query,
        limit: 10
      });
    } catch (error) {
      console.error('Error searching news:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSearch(searchQuery);
  };

  const openArticle = (url: string) => {
    if (url) {
      window.open(url, '_blank');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const highlightText = (text: string, query: string) => {
    if (!query) return text;
    
    const parts = text.split(new RegExp(`(${query})`, 'gi'));
    return parts.map((part, index) =>
      part.toLowerCase() === query.toLowerCase() ? (
        <mark key={index}>{part}</mark>
      ) : (
        part
      )
    );
  };

  if (loading && !data) {
    return (
      <div className="news-widget-loading">
        <div className="spinner"></div>
        <p>Searching news...</p>
      </div>
    );
  }

  return (
    <div className="news-widget search-widget">
      <div className="news-header">
        <div className="news-title">
          <h2>🔍 Search Results</h2>
          {data && <span className="news-count">{data.count} results</span>}
        </div>
      </div>

      <form onSubmit={handleSearchSubmit} className="search-form">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search news articles..."
          className="search-input"
        />
        <button type="submit" className="search-btn" disabled={loading}>
          {loading ? '⏳' : '🔍'} Search
        </button>
      </form>

      {data && data.query && (
        <div className="search-query-display">
          Showing results for: <strong>"{data.query}"</strong>
        </div>
      )}

      {data && data.articles.length === 0 ? (
        <div className="news-widget-empty">
          <p>No articles found for "{data.query}"</p>
          <p className="hint">Try different keywords or check spelling</p>
        </div>
      ) : (
        <div className="news-list">
          {data?.articles.map((article) => (
            <div key={article._id} className="news-card search-result-card">
              <div className="news-card-header">
                <h3 className="news-card-title">
                  {highlightText(article.title, data?.query || '')}
                </h3>
                <span className="news-category-badge">{article.category}</span>
              </div>

              <p className="news-card-content">
                {highlightText(
                  article.content.substring(0, 200) +
                    (article.content.length > 200 ? '...' : ''),
                  data?.query || ''
                )}
              </p>

              <div className="news-card-footer">
                <div className="news-meta">
                  <span className="news-source">📰 {article.source}</span>
                  <span className="news-date">
                    📅 {formatDate(article.published_date)}
                  </span>
                </div>
                {article.url && (
                  <button
                    onClick={() => openArticle(article.url!)}
                    className="read-more-btn"
                  >
                    Read More →
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Initialize the widget
const root = document.getElementById('news-search-root');
if (root) {
  createRoot(root).render(<NewsSearchWidget />);
}

// Type declarations
declare global {
  interface Window {
    openai?: {
      data?: any;
      onData?: (callback: (data: any) => void) => void;
      callTool?: (toolName: string, args: any) => Promise<void>;
      sendFollowupMessage?: (message: { prompt: string }) => Promise<void>;
      requestDisplayMode?: (mode: 'inline' | 'pip' | 'fullscreen') => Promise<void>;
    };
  }
}

export default NewsSearchWidget;
