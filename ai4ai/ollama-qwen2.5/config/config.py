import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Ollama settings
    OLLAMA_MODEL = "qwen2.5:3b"
    OLLAMA_HOST = "http://localhost:11434"
    
    # Yahoo Finance settings
    YAHOO_FINANCE_RSS = "https://finance.yahoo.com/news/rssindex"
    YAHOO_FINANCE_URL = "https://finance.yahoo.com/topic/stock-market-news"
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Scraping settings
    MAX_ARTICLES = 10
    REQUEST_TIMEOUT = 10
