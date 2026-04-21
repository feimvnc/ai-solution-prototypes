import requests
import feedparser
from bs4 import BeautifulSoup
from typing import List
import logging
from src.models.article import Article
from config.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YahooFinanceScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_rss_feed(self, max_articles: int = None) -> List[Article]:
        """Scrape Yahoo Finance RSS feed for news articles"""
        max_articles = max_articles or Config.MAX_ARTICLES
        articles = []
        
        try:
            logger.info("Fetching Yahoo Finance RSS feed...")
            feed = feedparser.parse(Config.YAHOO_FINANCE_RSS)
            
            for entry in feed.entries[:max_articles]:
                article = Article(
                    title=entry.get('title', 'No title'),
                    url=entry.get('link', ''),
                    published_date=entry.get('published', ''),
                    content=self._extract_content(entry.get('summary', ''))
                )
                articles.append(article)
                logger.info(f"Scraped: {article.title}")
            
            logger.info(f"Successfully scraped {len(articles)} articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error scraping RSS feed: {str(e)}")
            return []
    
    def scrape_article_content(self, url: str) -> str:
        """Scrape full article content from URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find article body
            article_body = soup.find('div', class_='caas-body')
            if article_body:
                paragraphs = article_body.find_all('p')
                content = ' '.join([p.get_text().strip() for p in paragraphs])
                return content
            
            # Fallback: get all paragraphs
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text().strip() for p in paragraphs[:10]])
            return content
            
        except Exception as e:
            logger.error(f"Error scraping article content from {url}: {str(e)}")
            return ""
    
    def _extract_content(self, html_summary: str) -> str:
        """Extract text content from HTML summary"""
        soup = BeautifulSoup(html_summary, 'html.parser')
        return soup.get_text().strip()
