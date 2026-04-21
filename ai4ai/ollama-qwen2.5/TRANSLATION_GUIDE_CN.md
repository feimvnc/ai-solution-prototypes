# 中文翻译功能说明

## 功能概述

Yahoo Finance News Analyzer 现在支持将英文内容和摘要翻译成中文！

## 使用方法

### 在Web界面中使用

1. **抓取并分析文章**
   - 点击 "Scrape & Analyze" 按钮获取文章和分析结果

2. **翻译内容**
   - 在每篇文章的内容（Content）和摘要（Summary）旁边，你会看到 "🇨🇳 翻译成中文" 按钮
   - 点击按钮即可将该部分翻译成中文
   - 翻译结果会显示在黄色背景的区域中
   - 再次点击按钮可以隐藏翻译结果

### 功能特点

- ✅ 使用本地 Ollama Qwen2.5 模型进行翻译
- ✅ 无需API密钥，完全本地运行
- ✅ 支持翻译文章内容和摘要
- ✅ 翻译结果可以显示/隐藏
- ✅ 翻译质量高，适合金融新闻

### API使用

如果你想通过API调用翻译功能：

```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple Inc. reported strong quarterly earnings today."}'
```

响应示例：
```json
{
  "status": "success",
  "translation": "苹果公司今日报告了强劲的季度收益。"
}
```

### Python代码示例

```python
import requests

url = "http://localhost:5000/api/translate"
data = {
    "text": "The stock market showed significant volatility."
}

response = requests.post(url, json=data)
result = response.json()

if result['status'] == 'success':
    print(f"翻译结果: {result['translation']}")
```

## 测试翻译功能

运行测试脚本：

```bash
cd ollama-qwen2.5
source venv/bin/activate
python test_translation.py
```

## 翻译示例

### 示例 1
**英文原文：**
> Apple Inc. reported strong quarterly earnings today, beating analyst expectations.

**中文翻译：**
> 苹果公司今日报告了强劲的季度收益，超出分析师预期。

### 示例 2
**英文原文：**
> The stock market showed significant volatility amid concerns about inflation.

**中文翻译：**
> 股市因对通胀的担忧而表现出显著的波动性。

### 示例 3
**英文原文：**
> Tesla's new electric vehicle model has received positive reviews from industry experts.

**中文翻译：**
> 特斯拉的新电动汽车模型受到了行业专家的积极评价。

## 技术实现

翻译功能使用 Qwen2.5 模型，该模型对中英文翻译有很好的支持：

- **模型：** qwen2.5:3b
- **温度参数：** 0.3（保证翻译准确性）
- **最大生成长度：** 500 tokens
- **处理时间：** 约2-3秒每次翻译

## 注意事项

1. **Ollama必须运行**
   - 确保 Ollama 服务正在运行
   - 确保已安装 qwen2.5:3b 模型

2. **翻译速度**
   - 翻译速度取决于你的硬件配置
   - 建议使用GPU加速以获得更快的翻译速度

3. **翻译质量**
   - Qwen2.5 对金融术语有很好的理解
   - 翻译结果准确且符合中文表达习惯

## 故障排除

### 翻译按钮无响应
- 检查浏览器控制台是否有错误
- 确认 Ollama 服务正在运行
- 刷新页面重试

### 翻译结果显示错误
- 检查 `logs/app.log` 查看详细错误信息
- 确认 Qwen2.5 模型已正确安装
- 重启 Ollama 服务

### 翻译速度慢
- 考虑使用更小的模型（如 qwen2.5:1.5b）
- 使用GPU加速
- 减少同时翻译的数量

## 未来改进

- [ ] 批量翻译多篇文章
- [ ] 支持更多语言（日语、韩语等）
- [ ] 缓存翻译结果
- [ ] 导出翻译后的内容
- [ ] 自定义翻译风格

---

**享受中文翻译功能！** 🇨🇳✨
