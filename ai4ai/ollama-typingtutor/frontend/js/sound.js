class SoundManager {
    constructor() {
        this.enabled = false;
        this.mode = 'letter'; // 'letter' or 'word'
        this.synth = window.speechSynthesis;
        this.currentWord = '';
        this.wordBuffer = [];
    }

    toggleSound() {
        this.enabled = !this.enabled;
        return this.enabled;
    }

    toggleMode() {
        this.mode = this.mode === 'letter' ? 'word' : 'letter';
        return this.mode;
    }

    speakLetter(char) {
        if (!this.enabled || this.mode !== 'letter') return;
        
        // Cancel any ongoing speech
        this.synth.cancel();
        
        const utterance = new SpeechSynthesisUtterance(char);
        utterance.rate = 1.2;
        utterance.pitch = 1.0;
        utterance.volume = 0.8;
        
        this.synth.speak(utterance);
    }

    addToWordBuffer(char) {
        if (!this.enabled || this.mode !== 'word') return;
        
        // Add character to buffer
        if (char === ' ' || char === '\n') {
            // Space or newline - speak the word
            if (this.currentWord.length > 0) {
                this.speakWord(this.currentWord);
                this.currentWord = '';
            }
        } else {
            this.currentWord += char;
        }
    }

    speakWord(word) {
        if (!this.enabled || this.mode !== 'word') return;
        
        // Cancel any ongoing speech
        this.synth.cancel();
        
        const utterance = new SpeechSynthesisUtterance(word);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 0.8;
        
        this.synth.speak(utterance);
    }

    speakCurrentWord() {
        if (this.currentWord.length > 0) {
            this.speakWord(this.currentWord);
            this.currentWord = '';
        }
    }

    reset() {
        this.synth.cancel();
        this.currentWord = '';
        this.wordBuffer = [];
    }

    handleKeyPress(char, isCorrect) {
        if (!this.enabled) return;

        if (this.mode === 'letter') {
            this.speakLetter(char);
        } else if (this.mode === 'word') {
            this.addToWordBuffer(char);
        }
    }
}
