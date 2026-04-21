const API_BASE = 'http://localhost:5001/api';

let keyboard, typingEngine, textRenderer, soundManager, translationManager;
let currentMode = 'text';
let allTexts = [];
let updateInterval;
let completedWords = new Set();

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    keyboard = new VirtualKeyboard('keyboard');
    typingEngine = new TypingEngine();
    textRenderer = new TextRenderer('text-display');
    soundManager = new SoundManager();
    translationManager = new TranslationManager();
    
    setupEventListeners();
    await checkHealth();
    await loadTexts();
}

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        const statusEl = document.getElementById('ai-status');
        if (data.ollama_connected) {
            statusEl.textContent = '🟢';
            statusEl.title = 'AI Connected';
        } else {
            statusEl.textContent = '🟡';
            statusEl.title = 'AI Disconnected';
        }
    } catch (error) {
        document.getElementById('ai-status').textContent = '🔴';
        console.error('Health check failed:', error);
    }
}

async function loadTexts() {
    try {
        const response = await fetch(`${API_BASE}/texts`);
        const data = await response.json();
        
        if (data.status === 'success') {
            allTexts = data.texts;
            renderTextGrid(allTexts);
        }
    } catch (error) {
        console.error('Error loading texts:', error);
    }
}

function renderTextGrid(texts) {
    const grid = document.getElementById('text-grid');
    grid.innerHTML = '';
    
    texts.forEach(text => {
        const card = document.createElement('div');
        card.className = 'text-card';
        card.innerHTML = `
            <div class="text-card-title">${text.title}</div>
            <span class="text-card-difficulty difficulty-${text.difficulty}">${text.difficulty}</span>
            <div class="text-card-preview">${text.text.substring(0, 100)}...</div>
        `;
        card.addEventListener('click', () => startTextPractice(text));
        grid.appendChild(card);
    });
}

function setupEventListeners() {
    document.querySelectorAll('.header-mode-btn').forEach(btn => {
        btn.addEventListener('click', () => switchMode(btn.dataset.mode));
    });
    
    document.querySelectorAll('.key-drill-btn').forEach(btn => {
        btn.addEventListener('click', () => startKeyDrill(btn.dataset.keys));
    });
    
    document.getElementById('generate-text-btn').addEventListener('click', generateAIText);
    document.getElementById('reset-btn').addEventListener('click', resetPractice);
    document.getElementById('finish-btn').addEventListener('click', finishPractice);
    document.getElementById('try-again-btn').addEventListener('click', tryAgain);
    document.getElementById('new-text-btn').addEventListener('click', newText);
    
    // Sound control buttons
    document.getElementById('sound-toggle').addEventListener('click', toggleSound);
    document.getElementById('sound-mode').addEventListener('click', toggleSoundMode);
    
    // Translation toggle button
    document.getElementById('translate-toggle').addEventListener('click', toggleTranslation);
    
    const typingInput = document.getElementById('typing-input');
    typingInput.addEventListener('input', handleTyping);
    typingInput.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace') {
            e.preventDefault();
        }
    });
}

function switchMode(mode) {
    currentMode = mode;
    
    document.querySelectorAll('.header-mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });
    
    document.getElementById('text-mode').classList.toggle('hidden', mode !== 'text');
    document.getElementById('key-mode').classList.toggle('hidden', mode !== 'keys');
    document.getElementById('ai-mode').classList.toggle('hidden', mode !== 'ai');
    document.getElementById('typing-area').classList.add('hidden');
    document.getElementById('ai-insights').classList.add('hidden');
}

function startTextPractice(text) {
    typingEngine.setText(text.text);
    textRenderer.render(text.text, 0);
    translationManager.setText(text.text);
    showTypingArea();
    keyboard.showNextKey(text.text[0]);
}

function startKeyDrill(keys) {
    let drillText;
    
    if (keys === 'numbers') {
        drillText = generateKeyDrillText('0123456789', 40);
    } else {
        drillText = generateKeyDrillText(keys, 50);
    }
    
    typingEngine.setText(drillText);
    textRenderer.render(drillText, 0);
    translationManager.setText(drillText);
    showTypingArea();
    keyboard.showNextKey(drillText[0]);
}

async function generateAIText() {
    const difficulty = document.getElementById('difficulty-select').value;
    const btn = document.getElementById('generate-text-btn');
    
    btn.disabled = true;
    btn.textContent = 'Generating...';
    
    try {
        const response = await fetch(`${API_BASE}/ai/generate-text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ difficulty })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            typingEngine.setText(data.text);
            textRenderer.render(data.text, 0);
            translationManager.setText(data.text);
            showTypingArea();
            keyboard.showNextKey(data.text[0]);
        }
    } catch (error) {
        console.error('Error generating text:', error);
        alert('Failed to generate text. Make sure Ollama is running.');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Generate Text';
    }
}

function showTypingArea() {
    document.getElementById('typing-area').classList.remove('hidden');
    document.getElementById('keyboard-legend').classList.remove('hidden');
    document.getElementById('typing-input').value = '';
    document.getElementById('typing-input').focus();
    completedWords.clear();
    resetStats();
}

async function handleTyping(e) {
    const input = e.target.value;
    const lastChar = input[input.length - 1];
    
    if (!lastChar) return;
    
    const result = typingEngine.processKey(lastChar);
    
    if (result.isCorrect) {
        keyboard.highlightKey(lastChar, 'correct');
        textRenderer.updateCurrent(result.currentIndex);
        
        // Play sound for correct keystroke
        soundManager.handleKeyPress(lastChar, true);
        
        // Check if word completed and show translation
        await checkAndShowTranslation(result.currentIndex);
        
        if (!result.isComplete) {
            keyboard.showNextKey(typingEngine.getCurrentChar());
        }
    } else {
        keyboard.highlightKey(lastChar, 'error');
        textRenderer.markError(result.currentIndex);
    }
    
    e.target.value = '';
    updateStats();
    
    if (result.isComplete) {
        document.getElementById('finish-btn').classList.remove('hidden');
        soundManager.speakCurrentWord(); // Speak final word if in word mode
    }
}

function updateStats() {
    if (!updateInterval) {
        updateInterval = setInterval(() => {
            const stats = typingEngine.getStats();
            document.getElementById('current-wpm').textContent = stats.wpm;
            document.getElementById('current-accuracy').textContent = stats.accuracy + '%';
            document.getElementById('current-time').textContent = stats.time + 's';
            document.getElementById('current-errors').textContent = stats.errors;
            
            document.getElementById('wpm-display').textContent = stats.wpm;
            document.getElementById('accuracy-display').textContent = stats.accuracy + '%';
        }, 1000);
    }
}

function resetStats() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
    
    document.getElementById('current-wpm').textContent = '0';
    document.getElementById('current-accuracy').textContent = '100%';
    document.getElementById('current-time').textContent = '0s';
    document.getElementById('current-errors').textContent = '0';
    document.getElementById('finish-btn').classList.add('hidden');
}

async function checkAndShowTranslation(charIndex) {
    if (!translationManager.enabled) return;
    
    const text = typingEngine.text;
    const nextChar = text[charIndex + 1];
    
    // Check if we just completed a word (next char is space or punctuation or end)
    if (!nextChar || !/[a-zA-Z]/.test(nextChar)) {
        const result = await translationManager.getTranslationForIndex(charIndex);
        
        if (result && result.translation && result.wordInfo) {
            const wordKey = `${result.wordInfo.startIndex}-${result.wordInfo.endIndex}`;
            
            // Only show translation once per word
            if (!completedWords.has(wordKey)) {
                completedWords.add(wordKey);
                showTranslationAboveWord(result.wordInfo, result.translation);
            }
        }
    }
}

function showTranslationAboveWord(wordInfo, translation) {
    const textDisplay = document.getElementById('text-display');
    const chars = textDisplay.querySelectorAll('.char');
    
    // Find the word span
    for (let i = wordInfo.startIndex; i <= wordInfo.endIndex; i++) {
        const charSpan = chars[i];
        if (charSpan) {
            // Wrap word in a container if not already wrapped
            if (!charSpan.parentElement.classList.contains('word')) {
                const wordSpan = document.createElement('span');
                wordSpan.className = 'word';
                
                // Collect all chars in this word
                const wordChars = [];
                for (let j = wordInfo.startIndex; j <= wordInfo.endIndex; j++) {
                    if (chars[j]) wordChars.push(chars[j]);
                }
                
                // Wrap them
                if (wordChars.length > 0) {
                    const parent = wordChars[0].parentElement;
                    parent.insertBefore(wordSpan, wordChars[0]);
                    wordChars.forEach(c => wordSpan.appendChild(c));
                    
                    // Add translation
                    const translationSpan = document.createElement('span');
                    translationSpan.className = 'translation';
                    translationSpan.textContent = translation;
                    wordSpan.appendChild(translationSpan);
                }
            }
            break;
        }
    }
}

function toggleTranslation() {
    const btn = document.getElementById('translate-toggle');
    const isEnabled = translationManager.toggleTranslation();
    
    if (isEnabled) {
        btn.setAttribute('data-translate', 'on');
        btn.title = 'Translation On';
        // Preload translations for current text
        if (typingEngine.text) {
            translationManager.setText(typingEngine.text);
        }
    } else {
        btn.setAttribute('data-translate', 'off');
        btn.title = 'Translation Off';
        // Remove all visible translations
        document.querySelectorAll('.translation').forEach(el => el.remove());
        completedWords.clear();
    }
}

function resetPractice() {
    typingEngine.reset();
    textRenderer.render(typingEngine.text, 0);
    keyboard.clearHighlights();
    keyboard.showNextKey(typingEngine.text[0]);
    document.getElementById('typing-input').value = '';
    document.getElementById('typing-input').focus();
    soundManager.reset();
    completedWords.clear();
    resetStats();
}

async function finishPractice() {
    const stats = typingEngine.finish();
    clearInterval(updateInterval);
    updateInterval = null;
    
    document.getElementById('final-wpm').textContent = stats.wpm;
    document.getElementById('final-accuracy').textContent = stats.accuracy + '%';
    document.getElementById('final-time').textContent = stats.time + 's';
    document.getElementById('final-errors').textContent = stats.errors;
    
    document.getElementById('results-modal').classList.remove('hidden');
    
    await getAIAnalysis(stats);
    await getAITips(stats);
}

async function getAIAnalysis(stats) {
    const analysisEl = document.getElementById('ai-analysis-text');
    analysisEl.textContent = 'Analyzing...';
    
    try {
        const response = await fetch(`${API_BASE}/ai/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stats })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            analysisEl.textContent = data.analysis;
        }
    } catch (error) {
        analysisEl.textContent = 'AI analysis unavailable. Great job on completing the practice!';
    }
}

async function getAITips(stats) {
    const insightsEl = document.getElementById('ai-insights');
    const contentEl = document.getElementById('insights-content');
    
    insightsEl.classList.remove('hidden');
    contentEl.innerHTML = '<p class="loading">Getting personalized tips...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/ai/tips`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                error_keys: stats.error_keys,
                wpm: stats.wpm,
                accuracy: stats.accuracy
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            contentEl.innerHTML = `<p>${data.tips.replace(/\n/g, '<br>')}</p>`;
        }
    } catch (error) {
        contentEl.innerHTML = '<p>Keep practicing to improve your speed and accuracy!</p>';
    }
}

function tryAgain() {
    document.getElementById('results-modal').classList.add('hidden');
    resetPractice();
}

function newText() {
    document.getElementById('results-modal').classList.add('hidden');
    document.getElementById('typing-area').classList.add('hidden');
    document.getElementById('keyboard-legend').classList.add('hidden');
    document.getElementById('ai-insights').classList.add('hidden');
    soundManager.reset();
    translationManager.reset();
    completedWords.clear();
    switchMode('text');
}

function toggleSound() {
    const btn = document.getElementById('sound-toggle');
    const modeBtn = document.getElementById('sound-mode');
    
    const isEnabled = soundManager.toggleSound();
    
    if (isEnabled) {
        btn.setAttribute('data-sound', 'on');
        btn.innerHTML = '🔊';
        btn.title = 'Sound On';
        modeBtn.classList.remove('disabled');
        modeBtn.disabled = false;
    } else {
        btn.setAttribute('data-sound', 'off');
        btn.innerHTML = '🔇';
        btn.title = 'Sound Off';
        modeBtn.classList.add('disabled');
        modeBtn.disabled = true;
        soundManager.reset();
    }
}

function toggleSoundMode() {
    if (!soundManager.enabled) return;
    
    const btn = document.getElementById('sound-mode');
    const mode = soundManager.toggleMode();
    
    if (mode === 'letter') {
        btn.setAttribute('data-mode', 'letter');
        btn.innerHTML = '🔤 Letter';
        btn.title = 'Letter Mode';
    } else {
        btn.setAttribute('data-mode', 'word');
        btn.innerHTML = '💬 Word';
        btn.title = 'Word Mode';
    }
    
    soundManager.reset();
}
