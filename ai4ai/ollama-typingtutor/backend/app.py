from flask import Flask
from flask_cors import CORS
import logging
import os

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {'message': 'Typing Tutor API', 'status': 'running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("🚀 Typing Tutor Backend API")
    print("="*60)
    print("📊 API running on: http://localhost:5000")
    print("⚠️  Make sure Ollama is running with qwen2.5:3b model")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
