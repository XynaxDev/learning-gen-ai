const messagesContainer = document.getElementById("messages");
const inputField = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const typingIndicator = document.getElementById("typing");

// Auto-resize textarea
inputField.addEventListener("input", function() {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});

// Handle Enter key
function handleKeyPress(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        send();
    }
}

// ROBUST FORMATTING FUNCTION - SPLIT STRATEGY
function formatMessage(text) {
    if (!text) return '';

    // 1. Split by code blocks
    const parts = text.split(/(```[\s\S]*?```)/g);

    return parts.map(part => {
        if (part.startsWith('```')) {
            const match = part.match(/```([\w-]*)\n?([\s\S]*?)```/);
            if (match) {
                const lang = match[1] || 'python'; // Default to python
                const code = match[2];
                return renderCodeBlock(lang, code);
            }
            return part; 
        } else {
            return formatText(part);
        }
    }).join('');
}

// Helper to format regular text
function formatText(text) {
    if (!text) return '';

    // Escape HTML first
    text = text.replace(/&/g, '&amp;')
               .replace(/</g, '&lt;')
               .replace(/>/g, '&gt;');

    // Format headers, bold, etc.
    text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/__(.+?)__/g, '<strong>$1</strong>');
    text = text.replace(/\*([^*\n]+?)\*/g, '<em>$1</em>');

    // Inline code (NOT block code)
    text = text.replace(/`([^`]+?)`/g, '<code>$1</code>');

    text = text.replace(/^[-*+] (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*?<\/li>\n?)+/gs, '<ul>$&</ul>');

    text = text.replace(/^-{3,}$/gm, '<hr>');
    text = text.replace(/^={3,}$/gm, '<hr>');

    return text.split('\n\n').map(segment => {
        if (!segment.trim()) return '';
        if (segment.match(/^<(ul|h1|h2|h3|hr)/)) return segment;
        return `<p>${segment.replace(/\n/g, '<br>')}</p>`;
    }).join('');
}

// Render code block using Prism syntax
function renderCodeBlock(lang, code) {
    // Escape HTML characters in the code content
    const safeCode = code
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Normalize language for Prism
    const prismLang = (lang.toLowerCase() === 'js' || lang.toLowerCase() === 'javascript') ? 'javascript' : 'python';

    return `<div class="code-block-wrapper">
        <div class="code-header">
            <span class="code-lang">${lang}</span>
            <button class="copy-btn" onclick="copyCode(this)">
                <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                Copy
            </button>
        </div>
        <pre><code class="language-${prismLang}">${safeCode}</code></pre>
    </div>`;
}

// Copy code function
window.copyCode = function(btn) {
    const wrapper = btn.closest('.code-block-wrapper');
    const code = wrapper.querySelector('code').textContent;

    navigator.clipboard.writeText(code).then(() => {
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!';
        btn.classList.add('copied');

        setTimeout(() => {
            btn.innerHTML = originalHTML;
            btn.classList.remove('copied');
        }, 2000);
    });
};

// Create bot avatar
function createBotAvatar() {
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar bot-avatar';
    avatar.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
    </svg>`;
    return avatar;
}

// Create user avatar
function createUserAvatar() {
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar user-avatar';
    avatar.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
    </svg>`;
    return avatar;
}

// Send message
async function send() {
    const text = inputField.value.trim();
    if (!text) return;

    // Remove welcome message
    const welcomeMsg = document.querySelector(".welcome-message");
    if (welcomeMsg) welcomeMsg.remove();

    // Add user message
    addMessage(text, "user");

    // Clear input
    inputField.value = "";
    inputField.style.height = "auto";

    // Disable send button
    sendBtn.disabled = true;

    // Show typing indicator
    typingIndicator.style.display = "flex";
    scrollToBottom();

    try {
        const API_URL =
            window.location.hostname === "localhost"
                ? "http://localhost:8000/chat"
                : "https://5jt2np51-8000.inc1.devtunnels.ms/chat";

        const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
        });

        if (!res.ok) throw new Error("Network response was not ok");

        const data = await res.json();

        // Hide typing indicator
        typingIndicator.style.display = "none";

        // Add bot message
        setTimeout(() => {
            addMessage(data.reply, "bot", data.timestamp);
        }, 400);

    } catch (error) {
        typingIndicator.style.display = "none";
        addMessage("Sorry, I'm having trouble connecting. Please try again.", "bot");
        console.error("Error:", error);
    } finally {
        sendBtn.disabled = false;
        inputField.focus();
    }
}

// Add message to chat
function addMessage(text, type, timestamp) {
    const wrapper = document.createElement("div");
    wrapper.className = `message-wrapper ${type}`;

    if (type === "bot") {
        wrapper.appendChild(createBotAvatar());
    } else {
        wrapper.appendChild(createUserAvatar());
    }

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";

    const msg = document.createElement("div");
    msg.className = `message ${type}`;

    if (type === "bot") {
        msg.innerHTML = formatMessage(text);
        // Highlight new code blocks
        requestAnimationFrame(() => {
            msg.querySelectorAll('pre code').forEach((block) => {
                Prism.highlightElement(block);
            });
        });
    } else {
        msg.textContent = text;
    }

    contentDiv.appendChild(msg);

    if (timestamp || type === "user") {
        const time = document.createElement("span");
        time.className = "timestamp";
        time.textContent = formatTime(timestamp);
        contentDiv.appendChild(time);
    }

    wrapper.appendChild(contentDiv);
    messagesContainer.appendChild(wrapper);

    scrollToBottom();
}

function formatTime(timestamp) {
    const date = timestamp ? new Date(timestamp) : new Date();
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function scrollToBottom() {
    setTimeout(() => {
        messagesContainer.scrollTo({
            top: messagesContainer.scrollHeight,
            behavior: "smooth"
        });
    }, 100);
}

window.addEventListener("load", () => {
    inputField.focus();
});