# Yahoo Finance News Analyzer with Ollama Qwen2.5

A web application that scrapes Yahoo Finance news, summarizes articles, and performs sentiment analysis using the local Ollama Qwen2.5 model.

## Features

- 📰 Scrape latest financial news from Yahoo Finance RSS feed
- 📝 Automatic text summarization using Qwen2.5
- 😊😐😟 Sentiment analysis (positive, negative, neutral)
- 🇨🇳 Translate content and summaries to Chinese
- 🌐 Clean web interface with Bootstrap
- 🔒 No API keys required - runs completely locally
- 🐍 Python virtual environment for isolation

## Project Structure

```
ollama-qwen2.5/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── config/
│   └── config.py              # Configuration settings
├── src/
│   ├── api/
│   │   └── routes.py          # Flask API routes
│   ├── models/
│   │   └── article.py         # Article data model
│   ├── scrapers/
│   │   └── yahoo_scraper.py   # Yahoo Finance scraper
│   ├── services/
│   │   └── ollama_service.py  # Ollama integration
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Custom styles
│   │   └── js/
│   │       └── app.js         # Frontend JavaScript
│   └── templates/
│       └── index.html         # Main HTML template
├── tests/                      # Unit tests (to be added)
└── logs/                       # Application logs

```

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running
3. **Qwen2.5 model** pulled in Ollama

### Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or download from: https://ollama.com/download
```

### Pull Qwen2.5 Model

```bash
ollama pull qwen2.5:latest
```

Verify Ollama is running:
```bash
ollama list
```

## Installation

1. **Navigate to project directory:**
```bash
cd ollama-qwen2.5
```

2. **Create virtual environment:**
```bash
python3 -m venv venv

$ python3 -V
Python 3.13.7
```

3. **Activate virtual environment:**
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

1. **Make sure Ollama is running:**
```bash
ollama serve
```

2. **Start the application:**
```bash
python app.py
```

3. **Open your browser:**
Navigate to `http://localhost:5000`

4. **Use the application:**
   - Set the number of articles to scrape (1-20)
   - Click "Scrape Only" to fetch news without analysis
   - Click "Scrape & Analyze" to fetch, summarize, and analyze sentiment
   - View results with summaries and sentiment badges

## API Endpoints

- `GET /` - Main web interface
- `GET /api/health` - Check Ollama connection status
- `POST /api/scrape` - Scrape news articles
  ```json
  {"max_articles": 5}
  ```
- `POST /api/analyze` - Analyze single article
  ```json
  {"text": "article text", "title": "article title"}
  ```
- `POST /api/scrape-and-analyze` - Scrape and analyze articles
  ```json
  {"max_articles": 5}
  ```
- `POST /api/translate` - Translate text to Chinese
  ```json
  {"text": "text to translate"}
  ```

## Configuration

Edit `config/config.py` to customize:

- `OLLAMA_MODEL` - Ollama model name (default: qwen2.5:latest)
- `OLLAMA_HOST` - Ollama server URL (default: http://localhost:11434)
- `MAX_ARTICLES` - Maximum articles to scrape (default: 10)
- `REQUEST_TIMEOUT` - HTTP request timeout (default: 10 seconds)

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Check if Qwen2.5 is installed: `ollama list`
- Verify Ollama is accessible: `curl http://localhost:11434/api/tags`

### Scraping Issues
- Yahoo Finance may block requests - wait a few minutes and try again
- Check your internet connection
- Review logs in `logs/app.log`

### Virtual Environment Issues
```bash
# Deactivate and recreate
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development

### Running Tests
```bash
# To be implemented
python -m pytest tests/
```

### Adding New Features
1. Add new scrapers in `src/scrapers/`
2. Add new services in `src/services/`
3. Add new routes in `src/api/routes.py`
4. Update models in `src/models/`

## Technologies Used

- **Backend:** Flask (Python web framework)
- **Scraping:** BeautifulSoup4, Feedparser, Requests
- **AI/ML:** Ollama with Qwen2.5 model
- **Frontend:** Bootstrap 5, Vanilla JavaScript
- **Data:** Python dataclasses

## License

MIT License - Feel free to use and modify

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Author

Built with ❤️ using Amazon Q Developer

## Notes

- This application runs completely locally - no external API calls for AI
- Sentiment analysis is performed by Qwen2.5 LLM
- News scraping respects Yahoo Finance's RSS feed
- All data is processed in real-time, no database storage by default
