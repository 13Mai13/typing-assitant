/**
 * Main Application - Typing Assistant
 */

// Initialize components
const keyboard = new KeyboardDisplay('keyboard-display');
const stats = new StatsDisplay();
const codePractice = new CodePractice();

let currentEngine = null;
let currentLesson = null;
let currentMode = 'lesson';

// API base URL
const API_BASE = '/api';

// Initialize app
async function init() {
    // Load default keyboard layout
    await keyboard.loadLayout('macos_standard');

    // Load lessons
    await loadLessons();

    // Setup event listeners
    setupEventListeners();
}

function setupEventListeners() {
    // Mode switching
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => switchMode(tab.dataset.mode));
    });

    // Keyboard layout selector
    document.getElementById('keyboard-layout').addEventListener('change', async (e) => {
        await keyboard.loadLayout(e.target.value);
    });

    // Lesson mode buttons
    document.getElementById('start-btn')?.addEventListener('click', startLesson);
    document.getElementById('restart-btn')?.addEventListener('click', restartLesson);
    document.getElementById('back-to-lessons-btn')?.addEventListener('click', backToLessons);

    // Code mode language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            await loadCodeProblems(btn.dataset.lang);
        });
    });

    // Code mode buttons
    document.getElementById('code-start-btn')?.addEventListener('click', startCodePractice);
    document.getElementById('code-restart-btn')?.addEventListener('click', restartCodePractice);
}

function switchMode(mode) {
    currentMode = mode;

    // Update active tab
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.mode === mode);
    });

    // Update visible content
    document.querySelectorAll('.mode-content').forEach(content => {
        content.classList.toggle('active', content.id === `${mode}-mode`);
    });

    // Generate heatmap and load stats when switching to stats mode
    if (mode === 'stats') {
        generateActivityHeatmap();
        loadDetailedStats();
    }

    // Reset stats and keyboard
    stats.reset();
    keyboard.clearHighlights();
    if (currentEngine) {
        currentEngine.stop();
        currentEngine = null;
    }
}

async function loadLessons() {
    try {
        const response = await fetch(`${API_BASE}/lessons`);
        const lessons = await response.json();

        const lessonList = document.getElementById('lesson-list');
        lessonList.innerHTML = '';

        lessons.forEach(lesson => {
            const lessonItem = document.createElement('div');
            lessonItem.className = 'lesson-item';
            if (!lesson.is_unlocked) {
                lessonItem.classList.add('locked');
            }

            lessonItem.innerHTML = `
                <h3>${lesson.name}</h3>
                <p>${lesson.description || ''}</p>
                <div class="lesson-meta">
                    <span>Keys: ${lesson.unlocked_keys.join(', ')}</span>
                    <span>Attempts: ${lesson.attempts}</span>
                    ${lesson.best_wpm ? `<span>Best: ${Math.round(lesson.best_wpm)} WPM</span>` : ''}
                </div>
            `;

            if (lesson.is_unlocked) {
                lessonItem.addEventListener('click', () => selectLesson(lesson));
            }

            lessonList.appendChild(lessonItem);
        });
    } catch (error) {
        console.error('Failed to load lessons:', error);
    }
}

async function selectLesson(lesson) {
    currentLesson = lesson;

    // Generate practice text
    try {
        const response = await fetch(`${API_BASE}/lessons/${lesson.id}/generate-text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ word_count: 50 }),
        });
        const data = await response.json();

        // Show typing area
        document.querySelector('.lesson-selector').style.display = 'none';
        document.getElementById('typing-area').classList.remove('hidden');

        // Display target text
        const targetText = document.getElementById('target-text');
        targetText.innerHTML = '';
        data.text.split('').forEach((char, i) => {
            const span = document.createElement('span');
            span.className = 'char';
            span.textContent = char;
            span.dataset.index = i;
            targetText.appendChild(span);
        });

        // Highlight first key
        keyboard.highlightNextKey(data.text[0]);

        // Show start button
        document.getElementById('start-btn').classList.remove('hidden');
    } catch (error) {
        console.error('Failed to generate practice text:', error);
    }
}

function startLesson() {
    const targetText = document.getElementById('target-text');
    const text = Array.from(targetText.querySelectorAll('.char'))
        .map(el => el.textContent)
        .join('');

    // Hide start button, show restart button
    document.getElementById('start-btn').classList.add('hidden');
    document.getElementById('restart-btn').classList.remove('hidden');

    // Create typing engine
    currentEngine = new TypingEngine(
        text,
        handleKeystroke,
        handleComplete
    );

    // Start engine and stats
    currentEngine.start();
    stats.start(currentEngine);

    // Highlight first character
    highlightCurrentChar(0);
}

function handleKeystroke(keystroke) {
    // Update character display
    const charSpan = document.querySelector(`.char[data-index="${keystroke.position}"]`);
    if (charSpan) {
        if (keystroke.correct) {
            charSpan.classList.add('correct');
            charSpan.classList.remove('cursor');

            // Highlight next character
            const nextIndex = keystroke.position + 1;
            highlightCurrentChar(nextIndex);
            keyboard.highlightNextKey(currentEngine.targetText[nextIndex]);
        } else {
            charSpan.classList.add('incorrect');
        }
    }

    // Show key press on keyboard
    keyboard.showKeyPress(keystroke.key, keystroke.correct);
}

function handleComplete(result) {
    stats.stop();
    keyboard.clearHighlights();

    // Calculate final metrics
    const accuracy = (result.correctKeystrokes / result.totalKeystrokes) * 100;
    const wpm = (result.correctKeystrokes / 5) / (result.duration / 60);

    alert(`Practice Complete!\n\nWPM: ${Math.round(wpm)}\nAccuracy: ${accuracy.toFixed(1)}%\nTime: ${Math.round(result.duration)}s`);
}

function highlightCurrentChar(index) {
    // Remove previous cursor
    document.querySelectorAll('.char.cursor').forEach(el => el.classList.remove('cursor'));

    // Add cursor to current char
    const charSpan = document.querySelector(`.char[data-index="${index}"]`);
    if (charSpan) {
        charSpan.classList.add('cursor');
    }
}

function restartLesson() {
    // Reset engine
    if (currentEngine) {
        currentEngine.stop();
        currentEngine = null;
    }

    // Reset stats
    stats.reset();
    stats.stop();

    // Reset text display
    document.querySelectorAll('.char').forEach(el => {
        el.classList.remove('correct', 'incorrect', 'cursor');
    });

    // Reset buttons
    document.getElementById('start-btn').classList.remove('hidden');
    document.getElementById('restart-btn').classList.add('hidden');

    // Reset keyboard
    keyboard.clearHighlights();
    const firstChar = document.querySelector('.char[data-index="0"]');
    if (firstChar) {
        keyboard.highlightNextKey(firstChar.textContent);
    }
}

function backToLessons() {
    // Stop current engine if running
    if (currentEngine) {
        currentEngine.stop();
        currentEngine = null;
    }

    // Reset stats
    stats.reset();
    stats.stop();

    // Clear keyboard
    keyboard.clearHighlights();

    // Show lesson selector, hide typing area
    document.querySelector('.lesson-selector').style.display = 'block';
    document.getElementById('typing-area').classList.add('hidden');

    // Reset current lesson
    currentLesson = null;
}

async function loadCodeProblems(language) {
    const problems = await codePractice.loadProblems(language);
    const problemList = document.getElementById('problem-list');
    codePractice.renderProblemList(problems, problemList);
}

function startCodePractice() {
    // TODO: Implement code practice mode
    console.log('Code practice not yet implemented');
}

function restartCodePractice() {
    // TODO: Implement code practice restart
    console.log('Code practice restart not yet implemented');
}

// Start the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
