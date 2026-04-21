class TypingEngine {
    constructor() {
        this.text = '';
        this.currentIndex = 0;
        this.errors = 0;
        this.startTime = null;
        this.endTime = null;
        this.isActive = false;
        this.errorKeys = [];
        this.keystrokes = [];
    }

    setText(text) {
        this.text = text;
        this.reset();
    }

    reset() {
        this.currentIndex = 0;
        this.errors = 0;
        this.startTime = null;
        this.endTime = null;
        this.isActive = false;
        this.errorKeys = [];
        this.keystrokes = [];
    }

    start() {
        if (!this.startTime) {
            this.startTime = Date.now();
            this.isActive = true;
        }
    }

    processKey(char) {
        if (!this.isActive) {
            this.start();
        }

        const expectedChar = this.text[this.currentIndex];
        const isCorrect = char === expectedChar;

        this.keystrokes.push({
            char: char,
            expected: expectedChar,
            correct: isCorrect,
            timestamp: Date.now()
        });

        if (!isCorrect) {
            this.errors++;
            if (!this.errorKeys.includes(expectedChar)) {
                this.errorKeys.push(expectedChar);
            }
        }

        if (isCorrect) {
            this.currentIndex++;
        }

        return {
            isCorrect,
            expectedChar,
            currentIndex: this.currentIndex,
            isComplete: this.currentIndex >= this.text.length
        };
    }

    finish() {
        this.endTime = Date.now();
        this.isActive = false;
        return this.getStats();
    }

    getStats() {
        const timeElapsed = (this.endTime || Date.now()) - (this.startTime || Date.now());
        const minutes = timeElapsed / 60000;
        const words = this.text.split(' ').length;
        const wpm = minutes > 0 ? Math.round(words / minutes) : 0;
        const accuracy = this.text.length > 0 
            ? Math.round(((this.text.length - this.errors) / this.text.length) * 100) 
            : 100;

        return {
            wpm,
            accuracy,
            time: Math.round(timeElapsed / 1000),
            errors: this.errors,
            total_words: words,
            time_spent: Math.round(timeElapsed / 1000),
            error_keys: this.errorKeys
        };
    }

    getCurrentChar() {
        return this.text[this.currentIndex] || '';
    }

    getProgress() {
        return this.text.length > 0 
            ? (this.currentIndex / this.text.length) * 100 
            : 0;
    }
}

class TextRenderer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    render(text, currentIndex) {
        this.container.innerHTML = '';
        
        for (let i = 0; i < text.length; i++) {
            const span = document.createElement('span');
            span.className = 'char';
            span.textContent = text[i];
            
            if (i < currentIndex) {
                span.classList.add('correct');
            } else if (i === currentIndex) {
                span.classList.add('current');
            }
            
            this.container.appendChild(span);
        }
    }

    markError(index) {
        const chars = this.container.querySelectorAll('.char');
        if (chars[index]) {
            chars[index].classList.remove('correct');
            chars[index].classList.add('incorrect');
        }
    }

    updateCurrent(index) {
        const chars = this.container.querySelectorAll('.char');
        chars.forEach((char, i) => {
            char.classList.remove('current');
            if (i === index) {
                char.classList.add('current');
            }
        });
    }
}

function generateKeyDrillText(keys, length = 50) {
    const keyArray = keys.split('');
    let text = '';
    
    for (let i = 0; i < length; i++) {
        text += keyArray[Math.floor(Math.random() * keyArray.length)];
        if (i % 5 === 4 && i < length - 1) {
            text += ' ';
        }
    }
    
    return text;
}
