#!/usr/bin/env python3
"""Final integration test - scrape and analyze 2 articles"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.scrapers.yahoo_scraper import YahooFinanceScraper
from src.services.ollama_service import OllamaService

def main():
    print("\n" + "="*70)
    print("🧪 FINAL INTEGRATION TEST - Yahoo Finance News Analyzer")
    print("="*70 + "\n")
    
    # Initialize services
    print("📡 Initializing services...")
    scraper = YahooFinanceScraper()
    ollama = OllamaService()
    
    # Check Ollama
    print("🔍 Checking Ollama connection...")
    if not ollama.check_connection():
        print("❌ Ollama not connected. Please start Ollama and try again.")
        return False
    print("✅ Ollama connected\n")
    
    # Scrape articles
    print("📰 Scraping 2 articles from Yahoo Finance...")
    articles = scraper.scrape_rss_feed(max_articles=2)
    
    if not articles:
        print("❌ Failed to scrape articles")
        return False
    
    print(f"✅ Scraped {len(articles)} articles\n")
    
    # Analyze each article
    for i, article in enumerate(articles, 1):
        print("-" * 70)
        print(f"📄 Article {i}: {article.title}")
        print(f"🔗 URL: {article.url}")
        print(f"📅 Published: {article.published_date}")
        
        # Get content
        text = article.content if article.content else article.title
        print(f"\n📝 Content preview: {text[:150]}...")
        
        # Summarize
        print("\n🤖 Generating summary...")
        summary = ollama.summarize(text)
        print(f"📋 Summary: {summary}")
        
        # Analyze sentiment
        print("\n😊 Analyzing sentiment...")
        sentiment = ollama.analyze_sentiment(text)
        emoji = "😊" if sentiment['sentiment'] == 'positive' else "😟" if sentiment['sentiment'] == 'negative' else "😐"
        print(f"{emoji} Sentiment: {sentiment['sentiment'].upper()} (score: {sentiment['score']})")
        print("-" * 70 + "\n")
    
    print("="*70)
    print("✅ INTEGRATION TEST COMPLETE - ALL SYSTEMS WORKING!")
    print("="*70)
    print("\n🚀 Ready to use! Start the application with:")
    print("   ./start.sh")
    print("\n   Then open: http://localhost:5000")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
