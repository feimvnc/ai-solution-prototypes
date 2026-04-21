class TranslationManager {
    constructor() {
        this.enabled = false;
        this.cache = new Map();
        this.currentText = '';
        this.words = [];
        this.API_BASE = 'http://localhost:5001/api';
    }

    toggleTranslation() {
        this.enabled = !this.enabled;
        return this.enabled;
    }

    setText(text) {
        this.currentText = text;
        this.words = this.extractWords(text);
        if (this.enabled) {
            this.preloadTranslations();
        }
    }

    extractWords(text) {
        const words = [];
        let currentWord = '';
        let startIndex = 0;

        for (let i = 0; i < text.length; i++) {
            const char = text[i];
            if (/[a-zA-Z]/.test(char)) {
                if (currentWord === '') {
                    startIndex = i;
                }
                currentWord += char;
            } else {
                if (currentWord) {
                    words.push({
                        word: currentWord.toLowerCase(),
                        startIndex: startIndex,
                        endIndex: i - 1
                    });
                    currentWord = '';
                }
            }
        }

        if (currentWord) {
            words.push({
                word: currentWord.toLowerCase(),
                startIndex: startIndex,
                endIndex: text.length - 1
            });
        }

        return words;
    }

    async preloadTranslations() {
        const uniqueWords = [...new Set(this.words.map(w => w.word))];
        
        for (const word of uniqueWords) {
            if (!this.cache.has(word)) {
                await this.translateWord(word);
            }
        }
    }

    async translateWord(word) {
        if (this.cache.has(word)) {
            return this.cache.get(word);
        }

        try {
            const response = await fetch(`${this.API_BASE}/ai/translate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ word })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.cache.set(word, data.translation);
                return data.translation;
            }
        } catch (error) {
            console.error('Translation error:', error);
        }

        return null;
    }

    async getTranslationForIndex(charIndex) {
        if (!this.enabled) return null;

        const wordInfo = this.words.find(w => 
            charIndex >= w.startIndex && charIndex <= w.endIndex
        );

        if (!wordInfo) return null;

        const translation = await this.translateWord(wordInfo.word);
        return {
            translation,
            wordInfo
        };
    }

    reset() {
        this.currentText = '';
        this.words = [];
    }
}
