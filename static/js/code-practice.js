/**
 * Code Practice - Handles code typing mode with syntax highlighting
 */

class CodePractice {
    constructor() {
        this.currentLanguage = 'python';
        this.problems = [];
        this.currentProblem = null;
    }

    async loadProblems(language) {
        try {
            this.currentLanguage = language;
            // TODO: Fetch from /api/code/problems?language={language}
            // For now, return empty array
            this.problems = [];
            return this.problems;
        } catch (error) {
            console.error('Failed to load code problems:', error);
            return [];
        }
    }

    async getProblem(problemId) {
        try {
            // TODO: Fetch from /api/code/problems/{problemId}
            return null;
        } catch (error) {
            console.error('Failed to load problem:', error);
            return null;
        }
    }

    renderProblemList(problems, container) {
        container.innerHTML = '';

        if (problems.length === 0) {
            container.innerHTML = '<p style="text-align: center; padding: 2rem;">No problems available yet. Coming soon!</p>';
            return;
        }

        problems.forEach(problem => {
            const item = document.createElement('div');
            item.className = 'problem-item';
            item.innerHTML = `
                <h3>${problem.title}</h3>
                <p>${problem.difficulty} - ${problem.category}</p>
            `;
            item.addEventListener('click', () => this.selectProblem(problem));
            container.appendChild(item);
        });
    }

    selectProblem(problem) {
        this.currentProblem = problem;
        // Trigger problem selection event
        document.dispatchEvent(new CustomEvent('problem-selected', { detail: problem }));
    }
}
