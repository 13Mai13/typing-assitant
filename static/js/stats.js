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
 * Load and display detailed statistics
 */
async function loadDetailedStats() {
    await loadStatsOverview();
    await loadSessionHistory();
    await loadKeyPerformance();
}

async function loadStatsOverview() {
    try {
        const response = await fetch('/api/stats/overview');
        const stats = await response.json();

        document.getElementById('total-sessions').textContent = stats.total_sessions;
        document.getElementById('avg-wpm').textContent = Math.round(stats.avg_wpm);
        document.getElementById('best-wpm').textContent = Math.round(stats.best_wpm);
        document.getElementById('completed-lessons').textContent = stats.completed_lessons;
    } catch (error) {
        console.error('Failed to load stats overview:', error);
    }
}

async function loadSessionHistory() {
    try {
        const response = await fetch('/api/stats/sessions?limit=10');
        const sessions = await response.json();

        const container = document.getElementById('session-history');
        container.innerHTML = '';

        if (sessions.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No sessions yet. Start practicing!</p>';
            return;
        }

        sessions.forEach(session => {
            const item = document.createElement('div');
            item.className = 'session-item';

            const date = new Date(session.started_at);
            const dateStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString();

            item.innerHTML = `
                <div>
                    <strong>${session.mode}</strong>
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">${dateStr}</div>
                </div>
                <div class="session-info">
                    <div class="session-metric">
                        <span class="session-metric-label">WPM</span>
                        <span class="session-metric-value">${Math.round(session.net_wpm)}</span>
                    </div>
                    <div class="session-metric">
                        <span class="session-metric-label">Accuracy</span>
                        <span class="session-metric-value">${session.accuracy.toFixed(1)}%</span>
                    </div>
                    <div class="session-metric">
                        <span class="session-metric-label">Duration</span>
                        <span class="session-metric-value">${Math.round(session.duration_seconds)}s</span>
                    </div>
                </div>
            `;
            container.appendChild(item);
        });
    } catch (error) {
        console.error('Failed to load session history:', error);
    }
}

async function loadKeyPerformance() {
    try {
        const response = await fetch('/api/stats/keys');
        const keys = await response.json();

        const container = document.getElementById('key-performance');
        container.innerHTML = '';

        if (keys.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No key data yet. Start practicing!</p>';
            return;
        }

        // Sort by confidence (lowest first) and take top 10
        const weakestKeys = keys
            .sort((a, b) => a.confidence_score - b.confidence_score)
            .slice(0, 10);

        weakestKeys.forEach(key => {
            const item = document.createElement('div');
            item.className = 'key-item';
            item.innerHTML = `
                <div class="key-char-display">${key.key_char}</div>
                <div class="key-stats">
                    <div class="key-stat">
                        <span class="key-stat-label">Accuracy</span>
                        <span class="key-stat-value">${key.accuracy.toFixed(1)}%</span>
                    </div>
                    <div class="key-stat">
                        <span class="key-stat-label">Attempts</span>
                        <span class="key-stat-value">${key.total_presses}</span>
                    </div>
                    <div class="key-stat">
                        <span class="key-stat-label">Avg Speed</span>
                        <span class="key-stat-value">${Math.round(key.avg_press_time)}ms</span>
                    </div>
                    <div class="key-stat">
                        <span class="key-stat-label">Confidence</span>
                        <span class="key-stat-value">${key.confidence_score.toFixed(2)}</span>
                    </div>
                </div>
            `;
            container.appendChild(item);
        });
    } catch (error) {
        console.error('Failed to load key performance:', error);
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
