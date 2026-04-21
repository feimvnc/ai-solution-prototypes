const keyboardLayout = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
    ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
    ['CapsLock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter'],
    ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
    ['Ctrl', 'Alt', ' ', 'Alt', 'Ctrl']
];

class VirtualKeyboard {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.keys = new Map();
        this.render();
    }

    render() {
        this.container.innerHTML = '';
        
        keyboardLayout.forEach((row, rowIndex) => {
            const rowDiv = document.createElement('div');
            rowDiv.className = 'keyboard-row';
            
            row.forEach(keyLabel => {
                const keyDiv = document.createElement('div');
                keyDiv.className = 'key';
                keyDiv.textContent = keyLabel === ' ' ? 'Space' : keyLabel;
                keyDiv.dataset.key = keyLabel.toLowerCase();
                
                if (keyLabel === ' ') {
                    keyDiv.classList.add('space');
                } else if (['Backspace', 'Tab', 'CapsLock', 'Enter', 'Shift', 'Ctrl', 'Alt'].includes(keyLabel)) {
                    keyDiv.classList.add('wide');
                }
                
                this.keys.set(keyLabel.toLowerCase(), keyDiv);
                rowDiv.appendChild(keyDiv);
            });
            
            this.container.appendChild(rowDiv);
        });
    }

    highlightKey(key, className = 'active') {
        const keyElement = this.keys.get(key.toLowerCase());
        if (keyElement) {
            keyElement.classList.remove('active', 'correct', 'error');
            keyElement.classList.add(className);
            
            // Remove animation class after animation completes
            setTimeout(() => {
                keyElement.classList.remove(className);
            }, 300);
        }
    }

    setKeyState(key, state) {
        const keyElement = this.keys.get(key.toLowerCase());
        if (keyElement) {
            keyElement.classList.remove('active', 'correct', 'error');
            if (state) {
                keyElement.classList.add(state);
            }
        }
    }

    clearHighlights() {
        this.keys.forEach(key => {
            key.classList.remove('active', 'correct', 'error');
        });
    }

    showNextKey(char) {
        this.clearHighlights();
        const keyElement = this.keys.get(char.toLowerCase());
        if (keyElement) {
            keyElement.classList.add('active');
        }
    }
}
