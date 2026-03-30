/**
 * Stats Display - Updates real-time statistics during typing
 */

class StatsDisplay {
    constructor() {
        this.wpmElement = document.getElementById('wpm-display');
        this.accuracyElement = document.getElementById('accuracy-display');
        this.timeElement = document.getElementById('time-display');
        this.updateInterval = null;
    }

    start(engine) {
        // Update stats every 100ms
        this.updateInterval = setInterval(() => {
            const metrics = engine.getMetrics();
            this.update(metrics);
        }, 100);
    }

    stop() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    update(metrics) {
        this.wpmElement.textContent = Math.round(metrics.wpm);
        this.accuracyElement.textContent = metrics.accuracy.toFixed(1);
        this.timeElement.textContent = this.formatTime(metrics.elapsed);
    }

    reset() {
        this.wpmElement.textContent = '0';
        this.accuracyElement.textContent = '100';
        this.timeElement.textContent = '0:00';
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}
