/**
 * Keyboard Display - Visualizes keyboard layouts and highlights keys
 */

class KeyboardDisplay {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.layout = null;
        this.currentLayout = 'macos_standard';
    }

    async loadLayout(layoutName) {
        try {
            // In a real implementation, this would fetch from /api/keyboards/{layoutName}
            // For now, we'll use a hardcoded basic layout
            this.currentLayout = layoutName;

            if (layoutName === 'macos_standard') {
                this.layout = this.getMacOSLayout();
            } else if (layoutName === 'corne_choc') {
                this.layout = this.getCorneLayout();
            }

            this.render();
        } catch (error) {
            console.error('Failed to load keyboard layout:', error);
        }
    }

    getMacOSLayout() {
        // Full macOS QWERTY layout with numbers and special characters
        return {
            name: 'macos_standard',
            type: 'standard',
            rows: [
                ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"],
                ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/'],
            ],
            homeKeys: ['f', 'j'],
        };
    }

    getCorneLayout() {
        // Corne Choc 36-key split keyboard
        return {
            name: 'corne_choc',
            type: 'split',
            leftHand: [
                ['q', 'w', 'e', 'r', 't'],
                ['a', 's', 'd', 'f', 'g'],
                ['z', 'x', 'c', 'v', 'b'],
            ],
            rightHand: [
                ['y', 'u', 'i', 'o', 'p'],
                ['h', 'j', 'k', 'l', ';'],
                ['n', 'm', ',', '.', '/'],
            ],
            homeKeys: ['f', 'j'],
        };
    }

    render() {
        if (!this.layout) return;

        this.container.innerHTML = '';

        if (this.layout.type === 'split') {
            this.renderSplitKeyboard();
        } else {
            this.renderStandardKeyboard();
        }
    }

    renderStandardKeyboard() {
        const keyboard = document.createElement('div');
        keyboard.className = 'keyboard';

        this.layout.rows.forEach(row => {
            const rowElement = document.createElement('div');
            rowElement.className = 'keyboard-row';

            row.forEach(key => {
                const keyElement = this.createKeyElement(key);
                rowElement.appendChild(keyElement);
            });

            keyboard.appendChild(rowElement);
        });

        this.container.appendChild(keyboard);
    }

    renderSplitKeyboard() {
        const keyboard = document.createElement('div');
        keyboard.className = 'keyboard split';

        // Left hand
        const leftHand = document.createElement('div');
        leftHand.className = 'keyboard-hand left';

        this.layout.leftHand.forEach(row => {
            const rowElement = document.createElement('div');
            rowElement.className = 'keyboard-row';

            row.forEach(key => {
                const keyElement = this.createKeyElement(key);
                rowElement.appendChild(keyElement);
            });

            leftHand.appendChild(rowElement);
        });

        // Right hand
        const rightHand = document.createElement('div');
        rightHand.className = 'keyboard-hand right';

        this.layout.rightHand.forEach(row => {
            const rowElement = document.createElement('div');
            rowElement.className = 'keyboard-row';

            row.forEach(key => {
                const keyElement = this.createKeyElement(key);
                rowElement.appendChild(keyElement);
            });

            rightHand.appendChild(rowElement);
        });

        keyboard.appendChild(leftHand);
        keyboard.appendChild(rightHand);
        this.container.appendChild(keyboard);
    }

    createKeyElement(keyChar) {
        const keyElement = document.createElement('div');
        keyElement.className = 'key';
        keyElement.dataset.key = keyChar;
        keyElement.textContent = keyChar;

        // Mark home row keys
        if (this.layout.homeKeys && this.layout.homeKeys.includes(keyChar)) {
            keyElement.classList.add('home');
        }

        return keyElement;
    }

    highlightNextKey(keyChar) {
        // Remove previous highlight
        this.container.querySelectorAll('.key.next').forEach(el => {
            el.classList.remove('next');
        });

        // Add highlight to next key
        const keyElement = this.container.querySelector(`[data-key="${keyChar}"]`);
        if (keyElement) {
            keyElement.classList.add('next');
        }
    }

    showKeyPress(keyChar, isCorrect) {
        const keyElement = this.container.querySelector(`[data-key="${keyChar}"]`);
        if (keyElement) {
            const className = isCorrect ? 'pressed' : 'error';
            keyElement.classList.add(className);

            // Remove class after animation
            setTimeout(() => {
                keyElement.classList.remove(className);
            }, 200);
        }
    }

    clearHighlights() {
        this.container.querySelectorAll('.key').forEach(el => {
            el.classList.remove('next', 'pressed', 'error');
        });
    }
}
