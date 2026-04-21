#!/bin/bash

echo "============================================================"
echo "🚀 Yahoo Finance News Analyzer"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  WARNING: Ollama is not running!"
    echo "Please start Ollama in another terminal:"
    echo "  ollama serve"
    echo ""
    echo "And make sure Qwen2.5 model is installed:"
    echo "  ollama pull qwen2.5:3b"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

echo "✅ Starting Flask application..."
echo "🌐 Open your browser and navigate to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python app.py
