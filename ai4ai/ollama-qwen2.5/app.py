import logging
import os

from config.config import Config
from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

    app.config.from_object(Config)

    # Setup logging
    if not os.path.exists(Config.LOGS_DIR):
        os.makedirs(Config.LOGS_DIR)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(Config.LOGS_DIR, "app.log")),
            logging.StreamHandler(),
        ],
    )

    # Register blueprints
    from src.api.routes import main_bp

    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    print("\n" + "=" * 60)
    print("🚀 Yahoo Finance News Analyzer")
    print("=" * 60)
    print("📊 Application starting...")
    print("🌐 Open your browser and navigate to: http://localhost:5001")
    print("⚠️  Make sure Ollama is running with Qwen2.5 model installed")
    print("=" * 60 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5001)
