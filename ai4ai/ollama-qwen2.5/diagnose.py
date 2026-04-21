#!/usr/bin/env python3
"""诊断脚本 - 检查翻译功能的所有组件"""

import os
import sys

def check_files():
    print("\n" + "="*70)
    print("📁 检查文件完整性")
    print("="*70 + "\n")
    
    files_to_check = [
        'src/services/ollama_service.py',
        'src/api/routes.py',
        'src/static/js/app.js',
        'src/static/css/style.css',
        'src/templates/index.html'
    ]
    
    all_exist = True
    for file in files_to_check:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"{status} {file}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_ollama_service():
    print("\n" + "="*70)
    print("🔍 检查Ollama服务代码")
    print("="*70 + "\n")
    
    with open('src/services/ollama_service.py', 'r') as f:
        content = f.read()
        has_translate = 'translate_to_chinese' in content
        print(f"{'✅' if has_translate else '❌'} translate_to_chinese 方法存在")
        return has_translate

def check_api_routes():
    print("\n" + "="*70)
    print("🔍 检查API路由")
    print("="*70 + "\n")
    
    with open('src/api/routes.py', 'r') as f:
        content = f.read()
        has_route = '/api/translate' in content
        has_function = 'def translate_to_chinese' in content
        print(f"{'✅' if has_route else '❌'} /api/translate 路由存在")
        print(f"{'✅' if has_function else '❌'} translate_to_chinese 函数存在")
        return has_route and has_function

def check_javascript():
    print("\n" + "="*70)
    print("🔍 检查JavaScript代码")
    print("="*70 + "\n")
    
    with open('src/static/js/app.js', 'r') as f:
        content = f.read()
        has_function = 'async function translateArticle' in content
        has_event = 'translate-btn' in content
        has_fetch = "fetch('/api/translate'" in content
        
        print(f"{'✅' if has_function else '❌'} translateArticle 函数存在")
        print(f"{'✅' if has_event else '❌'} translate-btn 类存在")
        print(f"{'✅' if has_fetch else '❌'} API调用代码存在")
        
        return has_function and has_event and has_fetch

def check_css():
    print("\n" + "="*70)
    print("🔍 检查CSS样式")
    print("="*70 + "\n")
    
    with open('src/static/css/style.css', 'r') as f:
        content = f.read()
        has_style = 'translation-text' in content
        print(f"{'✅' if has_style else '❌'} translation-text 样式存在")
        return has_style

def main():
    print("\n" + "="*70)
    print("🔧 翻译功能诊断工具")
    print("="*70)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    checks = {
        '文件完整性': check_files(),
        'Ollama服务': check_ollama_service(),
        'API路由': check_api_routes(),
        'JavaScript': check_javascript(),
        'CSS样式': check_css()
    }
    
    print("\n" + "="*70)
    print("📊 诊断结果")
    print("="*70 + "\n")
    
    all_passed = True
    for name, passed in checks.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    
    if all_passed:
        print("✅ 所有检查通过！翻译功能应该可以正常工作。")
        print("\n📝 使用步骤:")
        print("1. 启动应用: ./start.sh")
        print("2. 访问: http://localhost:5000")
        print("3. 点击 'Scrape & Analyze'")
        print("4. 点击 '🇨🇳 翻译成中文' 按钮")
        print("\n💡 如果仍然不工作，请:")
        print("- 打开浏览器开发者工具 (F12)")
        print("- 查看Console标签页的错误信息")
        print("- 查看Network标签页的API请求")
    else:
        print("❌ 某些检查失败。请修复上述问题。")
    
    print("="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
