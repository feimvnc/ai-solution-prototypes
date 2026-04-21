from flask import Blueprint, render_template, jsonify, request
from src.scrapers.yahoo_scraper import YahooFinanceScraper
from src.services.ollama_service import OllamaService
import logging

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

scraper = YahooFinanceScraper()
ollama_service = OllamaService()

@main_bp.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@main_bp.route('/test-translation')
def test_translation():
    """Render translation test page"""
    return render_template('test_translation.html')

@main_bp.route('/api/health')
def health_check():
    """Check if Ollama is running"""
    is_connected = ollama_service.check_connection()
    return jsonify({
        'status': 'ok' if is_connected else 'error',
        'ollama_connected': is_connected
    })

@main_bp.route('/api/scrape', methods=['POST'])
def scrape_news():
    """Scrape Yahoo Finance news"""
    try:
        data = request.get_json() or {}
        max_articles = data.get('max_articles', 5)
        
        logger.info(f"Scraping {max_articles} articles...")
        articles = scraper.scrape_rss_feed(max_articles=max_articles)
        
        return jsonify({
            'status': 'success',
            'count': len(articles),
            'articles': [article.to_dict() for article in articles]
        })
        
    except Exception as e:
        logger.error(f"Error in scrape_news: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/analyze', methods=['POST'])
def analyze_article():
    """Analyze a single article (summarize + sentiment)"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        title = data.get('title', '')
        
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'No text provided'
            }), 400
        
        logger.info(f"Analyzing article: {title}")
        
        # Generate summary
        summary = ollama_service.summarize(text)
        
        # Analyze sentiment
        sentiment_result = ollama_service.analyze_sentiment(text)
        
        return jsonify({
            'status': 'success',
            'summary': summary,
            'sentiment': sentiment_result['sentiment'],
            'sentiment_score': sentiment_result['score'],
            'sentiment_explanation': sentiment_result['explanation']
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_article: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/scrape-and-analyze', methods=['POST'])
def scrape_and_analyze():
    """Scrape news and analyze all articles"""
    try:
        data = request.get_json() or {}
        max_articles = data.get('max_articles', 5)
        
        logger.info(f"Scraping and analyzing {max_articles} articles...")
        articles = scraper.scrape_rss_feed(max_articles=max_articles)
        
        results = []
        for article in articles:
            # Use content or title for analysis
            text_to_analyze = article.content if article.content else article.title
            
            # Generate summary
            summary = ollama_service.summarize(text_to_analyze)
            
            # Analyze sentiment
            sentiment_result = ollama_service.analyze_sentiment(text_to_analyze)
            
            article.summary = summary
            article.sentiment = sentiment_result['sentiment']
            article.sentiment_score = sentiment_result['score']
            
            results.append(article.to_dict())
        
        return jsonify({
            'status': 'success',
            'count': len(results),
            'articles': results
        })
        
    except Exception as e:
        logger.error(f"Error in scrape_and_analyze: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/translate', methods=['POST'])
def translate_to_chinese():
    """Translate text to Chinese"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'No text provided'
            }), 400
        
        logger.info("Translating text to Chinese...")
        translation = ollama_service.translate_to_chinese(text)
        
        return jsonify({
            'status': 'success',
            'translation': translation
        })
        
    except Exception as e:
        logger.error(f"Error in translate_to_chinese: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
