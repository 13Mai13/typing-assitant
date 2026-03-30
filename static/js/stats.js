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

/**
 * Generate GitHub-style activity heatmap
 */
function generateActivityHeatmap() {
    const container = document.getElementById('activity-heatmap');
    if (!container) return;

    container.innerHTML = '';

    // Generate last 371 days (53 weeks)
    const today = new Date();
    const startDate = new Date(today);
    startDate.setDate(startDate.getDate() - 370);

    // Mock data - in real app, this would come from API
    const mockData = {};
    for (let i = 0; i < 371; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + i);
        const dateStr = date.toISOString().split('T')[0];
        // Random activity level (0-4) for demo
        mockData[dateStr] = Math.floor(Math.random() * 5);
    }

    // Create day cells
    for (let i = 0; i < 371; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + i);
        const dateStr = date.toISOString().split('T')[0];

        const day = document.createElement('div');
        day.className = 'heatmap-day';
        day.dataset.level = mockData[dateStr] || 0;
        day.title = `${dateStr}: ${mockData[dateStr] || 0} lessons`;

        container.appendChild(day);
    }
}
