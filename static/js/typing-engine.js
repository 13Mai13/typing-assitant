/**
 * Typing Engine - Handles real-time keystroke capture and validation
 */

class TypingEngine {
    constructor(targetText, onKeystroke, onComplete) {
        this.targetText = targetText;
        this.currentPosition = 0;
        this.onKeystroke = onKeystroke;
        this.onComplete = onComplete;
        this.startTime = null;
        this.keystrokes = [];
        this.isActive = false;
    }

    start() {
        this.startTime = Date.now();
        this.isActive = true;
        document.addEventListener('keydown', this.handleKeyPress.bind(this));
    }

    stop() {
        this.isActive = false;
        document.removeEventListener('keydown', this.handleKeyPress.bind(this));
    }

    handleKeyPress(event) {
        if (!this.isActive) return;

        // Ignore modifier keys and special keys
        if (event.ctrlKey || event.altKey || event.metaKey) return;
        if (event.key.length > 1 && event.key !== ' ') return;

        // Prevent default browser behavior
        event.preventDefault();

        const pressedKey = event.key;
        const expectedKey = this.targetText[this.currentPosition];
        const isCorrect = pressedKey === expectedKey;
        const timestamp = Date.now();

        const keystroke = {
            key: pressedKey,
            expected: expectedKey,
            correct: isCorrect,
            timestamp: timestamp,
            position: this.currentPosition,
            pressDuration: 0, // Will be calculated on keyup
        };

        this.keystrokes.push(keystroke);

        // Call callback for real-time updates
        if (this.onKeystroke) {
            this.onKeystroke(keystroke);
        }

        // Only advance on correct key (like keybr.com)
        if (isCorrect) {
            this.currentPosition++;

            // Check if completed
            if (this.currentPosition >= this.targetText.length) {
                this.complete();
            }
        }
    }

    complete() {
        this.stop();
        const endTime = Date.now();
        const duration = (endTime - this.startTime) / 1000; // seconds

        if (this.onComplete) {
            this.onComplete({
                keystrokes: this.keystrokes,
                duration: duration,
                totalKeystrokes: this.keystrokes.length,
                correctKeystrokes: this.keystrokes.filter(k => k.correct).length,
                incorrectKeystrokes: this.keystrokes.filter(k => !k.correct).length,
            });
        }
    }

    getMetrics() {
        if (!this.startTime) {
            return { wpm: 0, accuracy: 100, elapsed: 0 };
        }

        const total = this.keystrokes.length;
        const correct = this.keystrokes.filter(k => k.correct).length;
        const elapsed = (Date.now() - this.startTime) / 1000;

        // WPM calculation: (keystrokes / 5) / (time in minutes)
        const wpm = total > 0 ? (correct / 5) / (elapsed / 60) : 0;
        const accuracy = total > 0 ? (correct / total) * 100 : 100;

        return {
            wpm: Math.round(wpm * 10) / 10,
            accuracy: Math.round(accuracy * 10) / 10,
            elapsed: elapsed,
        };
    }

    reset() {
        this.currentPosition = 0;
        this.keystrokes = [];
        this.startTime = null;
        this.isActive = false;
    }
}
