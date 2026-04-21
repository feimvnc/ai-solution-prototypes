#!/usr/bin/env python3
"""Test script for AI Typing Tutor"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    print("\n" + "="*60)
    print("🧪 Testing Python Imports")
    print("="*60)
    
    try:
        import app
        print("✅ Flask app module import successful")
        
        from app.services.ollama_service import OllamaTypingAssistant
        print("✅ Ollama service import successful")
        
        from app.api.routes import api_bp
        print("✅ API routes import successful")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def test_data_files():
    print("\n" + "="*60)
    print("📁 Testing Data Files")
    print("="*60)
    
    texts_path = 'data/texts/classical_texts.json'
    
    if os.path.exists(texts_path):
        print(f"✅ Found {texts_path}")
        
        with open(texts_path, 'r') as f:
            texts = json.load(f)
            print(f"✅ Loaded {len(texts)} practice texts")
            
        return True
    else:
        print(f"❌ Missing {texts_path}")
        return False

def test_frontend_files():
    print("\n" + "="*60)
    print("🌐 Testing Frontend Files")
    print("="*60)
    
    files = [
        'frontend/index.html',
        'frontend/styles/main.css',
        'frontend/js/keyboard.js',
        'frontend/js/typing.js',
        'frontend/js/app.js'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ Missing {file}")
            all_exist = False
    
    return all_exist

def test_ollama_connection():
    print("\n" + "="*60)
    print("🤖 Testing Ollama Connection")
    print("="*60)
    
    try:
        from app.services.ollama_service import OllamaTypingAssistant
        assistant = OllamaTypingAssistant()
        
        if assistant.check_connection():
            print("✅ Ollama is connected")
            print("✅ Qwen2.5 model is available")
            return True
        else:
            print("⚠️  Ollama is not connected or model not found")
            print("   Please run: ollama serve")
            print("   And: ollama pull qwen2.5:3b")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_flask_app():
    print("\n" + "="*60)
    print("🚀 Testing Flask Application")
    print("="*60)
    
    try:
        # Import from backend/app.py
        import importlib.util
        spec = importlib.util.spec_from_file_location("app_module", "backend/app.py")
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        app = app_module.create_app()
        
        with app.test_client() as client:
            # Test root endpoint
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Root endpoint working")
            
            # Test health endpoint
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
                data = response.get_json()
                print(f"   Ollama connected: {data.get('ollama_connected')}")
            
            # Test texts endpoint
            response = client.get('/api/texts')
            if response.status_code == 200:
                print("✅ Texts endpoint working")
                data = response.get_json()
                print(f"   Loaded {len(data.get('texts', []))} texts")
            
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("🎹 AI Typing Tutor - Comprehensive Test Suite")
    print("="*60)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = {
        'Python Imports': test_imports(),
        'Data Files': test_data_files(),
        'Frontend Files': test_frontend_files(),
        'Ollama Connection': test_ollama_connection(),
        'Flask Application': test_flask_app()
    }
    
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    all_passed = True
    for name, passed in tests.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("✅ All tests passed! Application is ready to use.")
        print("\n📝 To start the application:")
        print("   ./start.sh")
        print("\n   Or manually:")
        print("   1. cd backend && source venv/bin/activate && python app.py")
        print("   2. Open frontend/index.html in your browser")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
