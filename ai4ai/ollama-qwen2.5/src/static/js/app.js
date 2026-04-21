// Check Ollama status on page load
document.addEventListener('DOMContentLoaded', function() {
    checkHealth();
});

async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        const statusIndicator = document.getElementById('status-indicator');
        if (data.ollama_connected) {
            statusIndicator.innerHTML = '<span class="badge bg-success">Ollama Connected ✓</span>';
        } else {
            statusIndicator.innerHTML = '<span class="badge bg-danger">Ollama Disconnected ✗</span>';
            showAlert('Ollama is not running. Please start Ollama and ensure Qwen2.5 model is installed.', 'danger');
        }
    } catch (error) {
        console.error('Health check failed:', error);
        document.getElementById('status-indicator').innerHTML = '<span class="badge bg-danger">Connection Error</span>';
    }
}

async function scrapeNews() {
    const maxArticles = document.getElementById('maxArticles').value;
    const scrapeBtn = document.getElementById('scrapeBtn');
    const spinner = document.getElementById('scrapeSpinner');
    
    scrapeBtn.disabled = true;
    spinner.classList.remove('d-none');
    
    try {
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ max_articles: parseInt(maxArticles) })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            displayArticles(data.articles, false);
            showAlert(`Successfully scraped ${data.count} articles!`, 'success');
        } else {
            showAlert('Error scraping articles: ' + data.message, 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error scraping articles: ' + error.message, 'danger');
    } finally {
        scrapeBtn.disabled = false;
        spinner.classList.add('d-none');
    }
}

async function scrapeAndAnalyze() {
    const maxArticles = document.getElementById('maxArticles').value;
    const analyzeBtn = document.getElementById('analyzeBtn');
    const spinner = document.getElementById('analyzeSpinner');
    
    analyzeBtn.disabled = true;
    spinner.classList.remove('d-none');
    
    showAlert('Scraping and analyzing articles... This may take a minute.', 'info');
    
    try {
        const response = await fetch('/api/scrape-and-analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ max_articles: parseInt(maxArticles) })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            displayArticles(data.articles, true);
            showAlert(`Successfully analyzed ${data.count} articles!`, 'success');
        } else {
            showAlert('Error analyzing articles: ' + data.message, 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error analyzing articles: ' + error.message, 'danger');
    } finally {
        analyzeBtn.disabled = false;
        spinner.classList.add('d-none');
    }
}

async function translateArticle(index, text, type, btnElement) {
    const resultId = `translation-${index}-${type}`;
    const resultDiv = document.getElementById(resultId);
    
    if (!text) {
        showAlert('No text to translate', 'warning');
        return;
    }
    
    // Toggle translation display
    if (resultDiv && !resultDiv.classList.contains('d-none')) {
        resultDiv.classList.add('d-none');
        btnElement.innerHTML = '🇨🇳 翻译成中文';
        return;
    }
    
    btnElement.disabled = true;
    btnElement.innerHTML = '<span class="spinner-border spinner-border-sm"></span> 翻译中...';
    
    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            if (resultDiv) {
                resultDiv.innerHTML = `<strong>🇨🇳 中文翻译：</strong><br>${data.translation}`;
                resultDiv.classList.remove('d-none');
                btnElement.innerHTML = '✓ 隐藏翻译';
            }
        } else {
            showAlert('Translation error: ' + data.message, 'danger');
            btnElement.innerHTML = '🇨🇳 翻译成中文';
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Translation error: ' + error.message, 'danger');
        btnElement.innerHTML = '🇨🇳 翻译成中文';
    } finally {
        btnElement.disabled = false;
    }
}

function displayArticles(articles, includeAnalysis) {
    const resultsDiv = document.getElementById('results');
    
    if (articles.length === 0) {
        resultsDiv.innerHTML = '<div class="alert alert-warning">No articles found.</div>';
        return;
    }
    
    let html = '<h4 class="mb-3">Results</h4>';
    
    articles.forEach((article, index) => {
        const sentimentClass = article.sentiment ? `sentiment-${article.sentiment}` : 'sentiment-neutral';
        const sentimentEmoji = article.sentiment === 'positive' ? '😊' : 
                              article.sentiment === 'negative' ? '😟' : '😐';
        
        html += `
            <div class="card article-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title mb-0">
                            <a href="${article.url}" target="_blank" class="article-title">
                                ${index + 1}. ${article.title}
                            </a>
                        </h5>
                        ${includeAnalysis && article.sentiment ? 
                            `<span class="badge ${sentimentClass} sentiment-badge">${sentimentEmoji} ${article.sentiment.toUpperCase()}</span>` 
                            : ''}
                    </div>
                    
                    ${article.published_date ? `<p class="text-muted small mb-2">📅 ${article.published_date}</p>` : ''}
                    
                    ${article.content ? `
                        <div class="content-text mb-2">
                            <strong>Content:</strong> ${article.content.substring(0, 300)}${article.content.length > 300 ? '...' : ''}
                            <button class="btn btn-sm btn-outline-primary ms-2 translate-btn" 
                                    data-index="${index}" 
                                    data-type="content" 
                                    data-text="${escapeHtml(article.content)}">
                                🇨🇳 翻译成中文
                            </button>
                            <div id="translation-${index}-content" class="translation-text d-none mt-2"></div>
                        </div>
                    ` : ''}
                    
                    ${includeAnalysis && article.summary ? `
                        <div class="summary-text">
                            <strong>📝 Summary:</strong><br>
                            ${article.summary}
                            <button class="btn btn-sm btn-outline-primary mt-2 translate-btn" 
                                    data-index="${index}" 
                                    data-type="summary" 
                                    data-text="${escapeHtml(article.summary)}">
                                🇨🇳 翻译成中文
                            </button>
                            <div id="translation-${index}-summary" class="translation-text d-none mt-2"></div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
    
    // Add event listeners to all translate buttons
    document.querySelectorAll('.translate-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const index = this.getAttribute('data-index');
            const type = this.getAttribute('data-type');
            const text = this.getAttribute('data-text');
            translateArticle(index, text, type, this);
        });
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showAlert(message, type) {
    const resultsDiv = document.getElementById('results');
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show alert-custom" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    resultsDiv.insertAdjacentHTML('afterbegin', alertHtml);
}
