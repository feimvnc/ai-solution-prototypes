#!/usr/bin/env python3
"""Test script to verify all components work"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.ollama_service import OllamaService
from src.scrapers.yahoo_scraper import YahooFinanceScraper

def test_ollama():
    print("=" * 60)
    print("Testing Ollama Connection...")
    print("=" * 60)
    
    service = OllamaService()
    is_connected = service.check_connection()
    
    if is_connected:
        print("✅ Ollama is connected and Qwen2.5 model is available!")
        
        # Test summarization
        print("\n" + "=" * 60)
        print("Testing Summarization...")
        print("=" * 60)
        test_text = "Apple Inc. reported strong quarterly earnings today, beating analyst expectations. The company's revenue increased by 15% year-over-year, driven by strong iPhone sales and growing services revenue."
        summary = service.summarize(test_text)
        print(f"Original: {test_text}")
        print(f"\nSummary: {summary}")
        
        # Test sentiment analysis
        print("\n" + "=" * 60)
        print("Testing Sentiment Analysis...")
        print("=" * 60)
        sentiment = service.analyze_sentiment(test_text)
        print(f"Sentiment: {sentiment['sentiment']}")
        print(f"Score: {sentiment['score']}")
        
        return True
    else:
        print("❌ Ollama is not connected or Qwen2.5 model is not available")
        print("Please run: ollama pull qwen2.5:3b")
        return False

def test_scraper():
    print("\n" + "=" * 60)
    print("Testing Yahoo Finance Scraper...")
    print("=" * 60)
    
    scraper = YahooFinanceScraper()
    articles = scraper.scrape_rss_feed(max_articles=3)
    
    if articles:
        print(f"✅ Successfully scraped {len(articles)} articles!")
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article.title}")
            print(f"   URL: {article.url}")
            print(f"   Content preview: {article.content[:100]}...")
        return True
    else:
        print("❌ Failed to scrape articles")
        return False

if __name__ == "__main__":
    print("\n🚀 Yahoo Finance News Analyzer - Component Test\n")
    
    ollama_ok = test_ollama()
    scraper_ok = test_scraper()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Ollama Service: {'✅ PASS' if ollama_ok else '❌ FAIL'}")
    print(f"Yahoo Scraper: {'✅ PASS' if scraper_ok else '❌ FAIL'}")
    
    if ollama_ok and scraper_ok:
        print("\n✅ All tests passed! Ready to run the application.")
        print("Run: python app.py")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
    
    print("=" * 60)
