from flask import Blueprint, jsonify, request
import json
import os
from app.services.ollama_service import OllamaTypingAssistant
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)
ollama_assistant = OllamaTypingAssistant()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Check API and Ollama health"""
    ollama_status = ollama_assistant.check_connection()
    return jsonify({
        'status': 'ok',
        'ollama_connected': ollama_status
    })

@api_bp.route('/texts', methods=['GET'])
def get_texts():
    """Get all classical texts"""
    try:
        texts_path = os.path.join(os.path.dirname(__file__), '../../../data/texts/classical_texts.json')
        with open(texts_path, 'r') as f:
            texts = json.load(f)
        return jsonify({'status': 'success', 'texts': texts})
    except Exception as e:
        logger.error(f"Error loading texts: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/texts/<int:text_id>', methods=['GET'])
def get_text(text_id):
    """Get specific text by ID"""
    try:
        texts_path = os.path.join(os.path.dirname(__file__), '../../../data/texts/classical_texts.json')
        with open(texts_path, 'r') as f:
            texts = json.load(f)
        
        text = next((t for t in texts if t['id'] == text_id), None)
        if text:
            return jsonify({'status': 'success', 'text': text})
        else:
            return jsonify({'status': 'error', 'message': 'Text not found'}), 404
    except Exception as e:
        logger.error(f"Error loading text: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/ai/tips', methods=['POST'])
def get_ai_tips():
    """Get AI-powered typing tips"""
    try:
        data = request.get_json()
        error_keys = data.get('error_keys', [])
        wpm = data.get('wpm', 0)
        accuracy = data.get('accuracy', 100)
        
        tips = ollama_assistant.get_typing_tips(error_keys, wpm, accuracy)
        
        return jsonify({
            'status': 'success',
            'tips': tips
        })
    except Exception as e:
        logger.error(f"Error getting AI tips: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/ai/generate-text', methods=['POST'])
def generate_practice_text():
    """Generate custom practice text with AI"""
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'medium')
        focus_keys = data.get('focus_keys', None)
        
        text = ollama_assistant.generate_practice_text(difficulty, focus_keys)
        
        return jsonify({
            'status': 'success',
            'text': text
        })
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/ai/analyze', methods=['POST'])
def analyze_session():
    """Analyze typing session with AI"""
    try:
        data = request.get_json()
        stats = data.get('stats', {})
        
        analysis = ollama_assistant.analyze_typing_pattern(stats)
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        })
    except Exception as e:
        logger.error(f"Error analyzing session: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/ai/translate', methods=['POST'])
def translate_word():
    """Translate English word to Chinese"""
    try:
        data = request.get_json()
        word = data.get('word', '')
        
        if not word:
            return jsonify({'status': 'error', 'message': 'No word provided'}), 400
        
        translation = ollama_assistant.translate_word(word)
        
        return jsonify({
            'status': 'success',
            'word': word,
            'translation': translation
        })
    except Exception as e:
        logger.error(f"Error translating word: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/stats', methods=['POST'])
def save_stats():
    """Save typing statistics"""
    try:
        data = request.get_json()
        # In a real app, save to database
        # For now, just return success
        return jsonify({
            'status': 'success',
            'message': 'Stats saved successfully'
        })
    except Exception as e:
        logger.error(f"Error saving stats: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
