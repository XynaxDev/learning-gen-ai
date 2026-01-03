// Global variables
const BACKEND_BASE_URL = 'http://localhost:8000';
let currentNotes = '';
let currentQuiz = [];
let mermaidCode = '';
let animationInterval = null;
let isAnimationPlaying = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkServerHealth();
    setupEventListeners();
    initializeMarked();
});

function initializeMarked() {
    // Configure marked.js for better markdown rendering
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            breaks: true,
            gfm: true,
            headerIds: true,
            mangle: false
        });
    }
}

function setupEventListeners() {
    document.getElementById('generate-btn').addEventListener('click', generateStudyMaterial);

    // Character counter for textarea
    const topicInput = document.getElementById('topic-input');
    topicInput.addEventListener('input', updateCharCount);

    // Allow Enter key in textarea with Ctrl/Cmd
    topicInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            generateStudyMaterial();
        }
    });

    // Hide mermaid image
    const mermaidImg = document.getElementById('mermaid-diagram');
    if (mermaidImg) {
        mermaidImg.style.display = 'none';
    }
}

function updateCharCount() {
    const text = document.getElementById('topic-input').value;
    const counter = document.getElementById('char-count');
    if (counter) {
        counter.textContent = text.length;
    }
}

async function checkServerHealth() {
    try {
        const response = await fetch(`${BACKEND_BASE_URL}/health`);
        const data = await response.json();
        updateStatus('ready', 'Ready');
        showToast('Server is ready!', 'success');
    } catch (error) {
        updateStatus('error', 'Server Offline');
        showToast('Cannot connect to server. Please start backend.py', 'error');
    }
}

function updateStatus(type, text) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.getElementById('status-text');

    statusDot.className = `status-dot ${type}`;
    statusText.textContent = text;
}

async function generateStudyMaterial() {
    const topicInput = document.getElementById('topic-input').value.trim();

    if (!topicInput) {
        showToast('Please enter a topic!', 'warning');
        return;
    }

    const useOllama = document.getElementById('use-ollama').checked;

    // Disable button and show loading
    const generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Generating...</span>';

    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    updateStatus('processing', 'Generating...');

    // Start loading animation
    animateLoadingSteps();

    try {
        const response = await fetch(`${BACKEND_BASE_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: topicInput,
                use_local_ollama: useOllama
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Store data
        currentNotes = data.notes;
        currentQuiz = data.quiz;
        mermaidCode = data.mermaid_code;

        // Display results
        displayNotes(data.notes);
        displayQuiz(data.quiz);
        displayVisualization();

        // Show results with animation
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('results').classList.remove('hidden');

        // Trigger fade-in animations
        setTimeout(() => {
            document.querySelectorAll('.fade-in').forEach((el, index) => {
                setTimeout(() => {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, index * 150);
            });
        }, 100);

        updateStatus('ready', 'Complete');
        showToast('Study material generated successfully!', 'success');

        // Scroll to results
        document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loading').classList.add('hidden');
        updateStatus('error', 'Error');

        let errorMessage = 'Failed to generate study material. Please try again.';
        if (error.message.includes('Connection refused') || error.message.includes('fetch')) {
            errorMessage = 'Cannot connect to server. Please check if the backend is running.';
        } else if (error.message.includes('timeout')) {
            errorMessage = 'Request timed out. The LLM might be taking too long to respond.';
        } else if (error.message) {
            errorMessage = `Error: ${error.message}`;
        }

        showToast(errorMessage, 'error');
    } finally {
        if (window.loadingInterval) {
            clearInterval(window.loadingInterval);
            window.loadingInterval = null;
        }

        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i> <span>Generate Study Material</span>';
    }
}

function animateLoadingSteps() {
    const steps = document.querySelectorAll('.loading-steps .step');

    steps.forEach(step => {
        step.classList.remove('active', 'completed');
        const icon = step.querySelector('.step-icon i');
        icon.className = 'fas fa-circle';
    });

    let currentStep = 0;

    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            steps[currentStep].classList.add('active');
            const icon = steps[currentStep].querySelector('.step-icon i');
            icon.className = 'fas fa-spinner fa-spin';

            if (currentStep > 0) {
                steps[currentStep - 1].classList.remove('active');
                steps[currentStep - 1].classList.add('completed');
                const prevIcon = steps[currentStep - 1].querySelector('.step-icon i');
                prevIcon.className = 'fas fa-check-circle';
            }

            currentStep++;
        } else {
            setTimeout(() => {
                steps.forEach((step, index) => {
                    step.classList.remove('active');
                    step.classList.add('completed');
                    const icon = step.querySelector('.step-icon i');
                    icon.className = 'fas fa-check-circle';
                });
            }, 500);
        }
    }, 1500);

    window.loadingInterval = interval;
}

function displayNotes(notes) {
    const notesContent = document.getElementById('notes-content');

    // Use marked.js if available for better markdown parsing
    if (typeof marked !== 'undefined') {
        let html = marked.parse(notes || '');
        notesContent.innerHTML = html;

        // Apply syntax highlighting to code blocks
        notesContent.querySelectorAll('pre code').forEach((block) => {
            // Add copy button to code blocks
            const pre = block.parentElement;
            const copyBtn = document.createElement('button');
            copyBtn.className = 'code-copy-btn';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.onclick = () => {
                navigator.clipboard.writeText(block.textContent);
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            };
            pre.style.position = 'relative';
            pre.insertBefore(copyBtn, block);

            // Apply syntax highlighting
            if (typeof hljs !== 'undefined') {
                hljs.highlightElement(block);
            }
        });
    } else {
        // Fallback to basic markdown rendering
        let formattedNotes = notes || '';

        formattedNotes = formattedNotes
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
            .replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>')
            .replace(/^### (.+)$/gm, '<h3>$1</h3>')
            .replace(/^## (.+)$/gm, '<h2>$1</h2>')
            .replace(/^# (.+)$/gm, '<h1>$1</h1>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/^[-•] (.+)$/gm, '<li>$1</li>')
            .replace(/\n\n+/g, '</p><p>')
            .replace(/(<li>.*?<\/li>)/gs, '<ul>$1</ul>');

        notesContent.innerHTML = formattedNotes;

        // Apply syntax highlighting to code blocks
        if (typeof hljs !== 'undefined') {
            notesContent.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        }
    }
}

function displayQuiz(quiz) {
    const quizContent = document.getElementById('quiz-content');
    quizContent.innerHTML = '';

    quiz.forEach((item, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'quiz-question';
        questionDiv.dataset.index = index;

        const questionHeader = document.createElement('div');
        questionHeader.className = 'question-header';

        const questionNumber = document.createElement('div');
        questionNumber.className = 'question-number';
        questionNumber.textContent = `Q${index + 1}`;

        const questionText = document.createElement('div');
        questionText.className = 'question-text';
        questionText.textContent = item.question;

        questionHeader.appendChild(questionNumber);
        questionHeader.appendChild(questionText);

        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'quiz-options';

        item.options.forEach((option, optIndex) => {
            const optionLabel = document.createElement('label');
            optionLabel.className = 'quiz-option';

            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = `question-${index}`;
            radio.value = option;
            radio.addEventListener('change', () => updateQuizScore());

            const optionCircle = document.createElement('span');
            optionCircle.className = 'option-circle';

            const optionText = document.createElement('span');
            optionText.className = 'option-text';
            optionText.textContent = option;

            optionLabel.appendChild(radio);
            optionLabel.appendChild(optionCircle);
            optionLabel.appendChild(optionText);
            optionsDiv.appendChild(optionLabel);
        });

        questionDiv.appendChild(questionHeader);
        questionDiv.appendChild(optionsDiv);
        quizContent.appendChild(questionDiv);
    });

    document.getElementById('quiz-score').textContent = `0/${quiz.length}`;
}

function updateQuizScore() {
    let correct = 0;
    currentQuiz.forEach((item, index) => {
        const selected = document.querySelector(`input[name="question-${index}"]:checked`);
        if (selected && selected.value === item.answer) {
            correct++;
        }
    });

    document.getElementById('quiz-score').textContent = `${correct}/${currentQuiz.length}`;
}

function checkAnswers() {
    const questions = document.querySelectorAll('.quiz-question');
    let allAnswered = true;
    let correct = 0;

    questions.forEach((question, index) => {
        const selected = question.querySelector('input:checked');
        const correctAnswer = currentQuiz[index].answer;

        if (!selected) {
            allAnswered = false;
            return;
        }

        question.classList.remove('correct', 'incorrect');
        const existingFeedback = question.querySelector('.answer-feedback');
        if (existingFeedback) existingFeedback.remove();

        const feedback = document.createElement('div');
        feedback.className = 'answer-feedback';

        if (selected.value === correctAnswer) {
            question.classList.add('correct');
            feedback.innerHTML = '<i class="fas fa-check-circle"></i> <span>Correct! Well done!</span>';
            feedback.classList.add('correct');
            correct++;
        } else {
            question.classList.add('incorrect');
            feedback.innerHTML = `<i class="fas fa-times-circle"></i> <span>Incorrect. The correct answer is: <strong>${correctAnswer}</strong></span>`;
            feedback.classList.add('incorrect');
        }

        question.appendChild(feedback);
    });

    if (!allAnswered) {
        showToast('Please answer all questions first!', 'warning');
        return;
    }

    updateQuizScore();

    const percentage = (correct / currentQuiz.length) * 100;
    let message = '';

    if (percentage === 100) {
        message = '🎉 Perfect score! You\'re a master!';
    } else if (percentage >= 80) {
        message = '🌟 Excellent work! Keep it up!';
    } else if (percentage >= 60) {
        message = '👍 Good job! Keep practicing!';
    } else {
        message = '📚 Review the notes and try again!';
    }

    showToast(message, 'success');
}

function startLangChainAnimation() {
    const nodeMap = {
        input: document.querySelector('.chain-node[data-node="input"]'),
        notes: document.querySelector('.chain-node[data-node="notes"]'),
        quiz: document.querySelector('.chain-node[data-node="quiz"]'),
        merge: document.querySelector('.chain-node[data-node="merge"]'),
        output: document.querySelector('.chain-node[data-node="output"]'),
    };

    const allNodes = Object.values(nodeMap).filter(Boolean);
    const particles = document.querySelectorAll('.flow-particle');

    const groups = [
        ['input'],
        ['notes', 'quiz'],
        ['merge'],
        ['output'],
    ];

    allNodes.forEach((node) => {
        node.classList.remove('active', 'completed');
    });

    let currentGroup = 0;

    const chainInterval = setInterval(() => {
        if (currentGroup > 0) {
            const prevKeys = groups[currentGroup - 1];
            prevKeys.forEach((key) => {
                const node = nodeMap[key];
                if (!node) return;
                node.classList.remove('active');
                node.classList.add('completed');
            });
        }

        if (currentGroup >= groups.length) {
            clearInterval(chainInterval);
            window.chainAnimationInterval = null;
            return;
        }

        const keys = groups[currentGroup];
        keys.forEach((key) => {
            const node = nodeMap[key];
            if (!node) return;
            node.classList.add('active');
        });

        particles.forEach((p) => {
            p.style.animation = 'none';
            setTimeout(() => {
                p.style.animation = 'flowParticle 1.2s ease-in-out';
            }, 10);
        });

        currentGroup += 1;
    }, 1200);

    window.chainAnimationInterval = chainInterval;
}

function stopLangChainAnimation() {
    if (window.chainAnimationInterval) {
        clearInterval(window.chainAnimationInterval);
        window.chainAnimationInterval = null;
    }
}

function displayVisualization() {
    const img = document.getElementById('mermaid-diagram');
    if (img) {
        img.style.display = 'none';
    }

    const chainAnimation = document.getElementById('chain-animation');
    if (chainAnimation) {
        chainAnimation.style.display = 'block';
    }

    startLangChainAnimation();
}

function clearOutput() {
    currentNotes = '';
    currentQuiz = [];
    mermaidCode = '';

    document.getElementById('notes-content').innerHTML = '';
    document.getElementById('quiz-content').innerHTML = '';
    document.getElementById('quiz-score').textContent = '0/0';

    document.getElementById('results').classList.add('hidden');
    document.getElementById('topic-input').value = '';
    document.getElementById('topic-input').focus();
    updateCharCount();

    stopAnimation();
    stopLangChainAnimation();

    window.scrollTo({ top: 0, behavior: 'smooth' });
    showToast('Output cleared!', 'info');
}

function toggleAnimation() {
    const btn = document.querySelector('#anim-toggle');

    if (!isAnimationPlaying) {
        startAnimation();
        btn.textContent = 'Pause';
        btn.parentElement.querySelector('i').className = 'fas fa-pause';
        isAnimationPlaying = true;
    } else {
        stopAnimation();
        btn.textContent = 'Play';
        btn.parentElement.querySelector('i').className = 'fas fa-play';
        isAnimationPlaying = false;
    }
}

function startAnimation() {
    stopLangChainAnimation();
    startLangChainAnimation();
}

function stopAnimation() {
    stopLangChainAnimation();
    isAnimationPlaying = false;
}

function copyNotes(format) {
    let textToCopy = currentNotes;

    if (format === 'plain') {
        textToCopy = currentNotes
            .replace(/\*\*(.*?)\*\*/g, '$1')
            .replace(/\*(.*?)\*/g, '$1')
            .replace(/^#+\s/gm, '')
            .replace(/```[\s\S]*?```/g, '')
            .replace(/`([^`]+)`/g, '$1')
            .trim();
    }

    navigator.clipboard.writeText(textToCopy).then(() => {
        showToast(`Notes copied as ${format}!`, 'success');
    }).catch(() => {
        showToast('Failed to copy notes', 'error');
    });
}

function downloadVisualization() {
    const img = document.getElementById('mermaid-diagram');

    if (!img.src || img.src === window.location.href) {
        showToast('No visualization available to download', 'warning');
        return;
    }

    const link = document.createElement('a');
    link.href = img.src;
    link.download = 'langchain-visualization.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showToast('Visualization downloaded!', 'success');
}

function resetForNextTopic() {
    document.getElementById('topic-input').value = '';
    document.getElementById('results').classList.add('hidden');
    document.getElementById('topic-input').focus();
    updateCharCount();

    window.scrollTo({ top: 0, behavior: 'smooth' });

    stopAnimation();
    stopLangChainAnimation();

    showToast('Ready for next topic!', 'info');
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    toast.innerHTML = `
        <div class="toast-icon">
            <i class="fas ${icons[type]}"></i>
        </div>
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    container.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentElement) {
                container.removeChild(toast);
            }
        }, 300);
    }, 5000);
}