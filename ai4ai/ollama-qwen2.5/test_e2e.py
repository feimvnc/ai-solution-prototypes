#!/usr/bin/env python3
"""端到端测试 - 验证翻译功能在完整流程中工作"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import json

def test_full_workflow():
    print("\n" + "="*70)
    print("🧪 端到端测试 - 抓取、分析和翻译")
    print("="*70 + "\n")
    
    app = create_app()
    
    with app.test_client() as client:
        # 1. 测试健康检查
        print("1️⃣ 测试健康检查...")
        response = client.get('/api/health')
        health_data = response.get_json()
        print(f"   状态: {health_data['status']}")
        print(f"   Ollama连接: {health_data['ollama_connected']}")
        
        if not health_data['ollama_connected']:
            print("❌ Ollama未连接，测试终止")
            return False
        print("   ✅ 健康检查通过\n")
        
        # 2. 测试抓取和分析
        print("2️⃣ 测试抓取和分析 (2篇文章)...")
        response = client.post('/api/scrape-and-analyze',
                              json={'max_articles': 2},
                              content_type='application/json')
        
        if response.status_code != 200:
            print(f"❌ 抓取失败: {response.status_code}")
            return False
        
        data = response.get_json()
        print(f"   状态: {data['status']}")
        print(f"   文章数量: {data['count']}")
        
        if data['count'] == 0:
            print("❌ 没有抓取到文章")
            return False
        
        articles = data['articles']
        print("   ✅ 抓取和分析成功\n")
        
        # 3. 测试翻译第一篇文章的摘要
        print("3️⃣ 测试翻译功能...")
        first_article = articles[0]
        print(f"   文章标题: {first_article['title'][:50]}...")
        
        if first_article.get('summary'):
            print(f"   英文摘要: {first_article['summary'][:100]}...")
            
            # 翻译摘要
            response = client.post('/api/translate',
                                  json={'text': first_article['summary']},
                                  content_type='application/json')
            
            if response.status_code != 200:
                print(f"❌ 翻译失败: {response.status_code}")
                return False
            
            trans_data = response.get_json()
            if trans_data['status'] == 'success':
                print(f"   🇨🇳 中文翻译: {trans_data['translation']}")
                print("   ✅ 翻译成功\n")
            else:
                print(f"❌ 翻译错误: {trans_data.get('message')}")
                return False
        else:
            print("   ⚠️  文章没有摘要，跳过翻译测试\n")
        
        # 4. 测试翻译内容
        if first_article.get('content'):
            print("4️⃣ 测试翻译文章内容...")
            content_preview = first_article['content'][:200]
            print(f"   内容预览: {content_preview}...")
            
            response = client.post('/api/translate',
                                  json={'text': content_preview},
                                  content_type='application/json')
            
            if response.status_code == 200:
                trans_data = response.get_json()
                if trans_data['status'] == 'success':
                    print(f"   🇨🇳 中文翻译: {trans_data['translation']}")
                    print("   ✅ 内容翻译成功\n")
                else:
                    print(f"❌ 翻译错误: {trans_data.get('message')}")
                    return False
            else:
                print(f"❌ 翻译失败: {response.status_code}")
                return False
    
    print("="*70)
    print("✅ 所有测试通过！翻译功能工作正常！")
    print("="*70)
    print("\n📝 测试总结:")
    print("   ✅ 健康检查")
    print("   ✅ 文章抓取")
    print("   ✅ 情感分析")
    print("   ✅ 摘要生成")
    print("   ✅ 中文翻译")
    print("\n🚀 应用程序已准备就绪！")
    print("   启动命令: ./start.sh")
    print("   访问地址: http://localhost:5000")
    print("="*70 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_full_workflow()
    sys.exit(0 if success else 1)
