#!/usr/bin/env python3
"""测试翻译功能"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.ollama_service import OllamaService

def test_translation():
    print("\n" + "="*70)
    print("🧪 测试中文翻译功能")
    print("="*70 + "\n")
    
    service = OllamaService()
    
    # 检查Ollama连接
    print("🔍 检查Ollama连接...")
    if not service.check_connection():
        print("❌ Ollama未连接。请启动Ollama并重试。")
        return False
    print("✅ Ollama已连接\n")
    
    # 测试翻译
    test_texts = [
        "Apple Inc. reported strong quarterly earnings today, beating analyst expectations.",
        "The stock market showed significant volatility amid concerns about inflation.",
        "Tesla's new electric vehicle model has received positive reviews from industry experts."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print("-" * 70)
        print(f"📝 测试 {i}:")
        print(f"英文原文: {text}")
        print("\n🤖 翻译中...")
        
        translation = service.translate_to_chinese(text)
        print(f"🇨🇳 中文翻译: {translation}")
        print("-" * 70 + "\n")
    
    print("="*70)
    print("✅ 翻译功能测试完成！")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_translation()
    sys.exit(0 if success else 1)
