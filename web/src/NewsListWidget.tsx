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

interface NewsData {
  articles: Article[];
  category: string;
  count: number;
  days_back: number;
}

function NewsListWidget() {
  const [data, setData] = useState<NewsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get data from window.openai
    const loadData = async () => {
      try {
        if (window.openai?.data) {
          setData(window.openai.data as NewsData);
        }
      } catch (error) {
        console.error('Error loading news data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadData();

    // Listen for data updates
    window.openai?.onData?.((newData: NewsData) => {
      setData(newData);
    });
  }, []);

  const handleRefresh = async () => {
    setLoading(true);
    try {
      await window.openai?.callTool('fetch_news', {
        category: data?.category === 'All' ? '' : data?.category,
        limit: 10,
        daysBack: data?.days_back || 7
      });
    } catch (error) {
      console.error('Error refreshing news:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = async (category: string) => {
    setLoading(true);
    try {
      await window.openai?.callTool('fetch_news', {
        category: category === 'All' ? '' : category,
        limit: 10,
        daysBack: data?.days_back || 7
      });
    } catch (error) {
      console.error('Error changing category:', error);
    } finally {
      setLoading(false);
    }
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

  if (loading) {
    return (
      <div className="news-widget-loading">
        <div className="spinner"></div>
        <p>Loading news...</p>
      </div>
    );
  }

  if (!data || data.articles.length === 0) {
    return (
      <div className="news-widget-empty">
        <p>No news articles found</p>
        <button onClick={handleRefresh} className="refresh-btn">
          Refresh
        </button>
      </div>
    );
  }

  return (
    <div className="news-widget">
      <div className="news-header">
        <div className="news-title">
          <h2>📰 {data.category} News</h2>
          <span className="news-count">{data.count} articles</span>
        </div>
        <button onClick={handleRefresh} className="refresh-btn" disabled={loading}>
          🔄 Refresh
        </button>
      </div>

      <div className="news-list">
        {data.articles.map((article) => (
          <div key={article._id} className="news-card">
            <div className="news-card-header">
              <h3 className="news-card-title">{article.title}</h3>
              <span className="news-category-badge">{article.category}</span>
            </div>

            <p className="news-card-content">
              {article.content.substring(0, 200)}
              {article.content.length > 200 ? '...' : ''}
            </p>

            <div className="news-card-footer">
              <div className="news-meta">
                <span className="news-source">📰 {article.source}</span>
                <span className="news-date">📅 {formatDate(article.published_date)}</span>
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
    </div>
  );
}

// Initialize the widget
const root = document.getElementById('news-list-root');
if (root) {
  createRoot(root).render(<NewsListWidget />);
}

// Type declarations for window.openai
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

export default NewsListWidget;
