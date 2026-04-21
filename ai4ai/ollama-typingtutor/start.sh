#!/bin/bash

echo "============================================================"
echo "🎹 AI Typing Tutor - Startup Script"
echo "============================================================"
echo ""

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

# Start backend
echo "🚀 Starting backend server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

echo "Backend started with PID: $BACKEND_PID"
echo ""
echo "============================================================"
echo "✅ Application is running!"
echo "============================================================"
echo "📊 Backend API: http://localhost:5001"
echo "🌐 Frontend: Open frontend/index.html in your browser"
echo ""
echo "Or start a simple HTTP server for frontend:"
echo "  cd frontend && python3 -m http.server 8000"
echo "  Then visit: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the backend server"
echo "============================================================"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID; exit" INT
wait $BACKEND_PID
