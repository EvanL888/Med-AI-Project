// --- Scan Button Animation ---
window.addEventListener('DOMContentLoaded', function() {
    const scanBtn = document.getElementById('scan-btn');
    const scanBeam = document.getElementById('scan-beam');
    if (scanBtn && scanBeam) {
        scanBtn.onclick = function() {
            scanBeam.style.opacity = '1';
            scanBeam.style.height = '100vh';
            setTimeout(function() {
                scanBeam.style.opacity = '0';
                scanBeam.style.height = '0';
            }, 1200);
        };
    }
});

// --- ER Chatbot UI Logic ---
const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const restartBtn = document.getElementById('restart-btn');
const goBackBtn = document.getElementById('go-back-btn');

// SVGs for icons
// Stylized robot face SVG (modern, friendly)
const botSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 48 48" fill="none"><rect width="48" height="48" rx="24" fill="#4f8cff"/><ellipse cx="24" cy="28" rx="12" ry="8" fill="#fff"/><ellipse cx="17.5" cy="21.5" rx="3.5" ry="4.5" fill="#fff"/><ellipse cx="30.5" cy="21.5" rx="3.5" ry="4.5" fill="#fff"/><ellipse cx="17.5" cy="22" rx="1.5" ry="2" fill="#23234a"/><ellipse cx="30.5" cy="22" rx="1.5" ry="2" fill="#23234a"/><rect x="20" y="32" width="8" height="2" rx="1" fill="#23234a"/></svg>`;
// Neutral human avatar SVG (friendly silhouette)
const patientSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 48 48" fill="none"><rect width="48" height="48" rx="24" fill="#43a047"/><ellipse cx="24" cy="20" rx="8" ry="8" fill="#fff"/><ellipse cx="24" cy="36" rx="14" ry="8" fill="#fff" fill-opacity="0.85"/></svg>`;

function appendMessage(sender, text) {
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'er-bubble ' + (sender === 'bot' ? 'bot' : 'patient');
    // Icon
    const iconDiv = document.createElement('div');
    iconDiv.className = sender === 'bot' ? 'er-bot-icon' : 'er-patient-icon';
    iconDiv.innerHTML = sender === 'bot' ? botSVG : patientSVG;
    // Bubble content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'er-bubble-content';
    contentDiv.textContent = text;
    bubbleDiv.appendChild(iconDiv);
    bubbleDiv.appendChild(contentDiv);
    chatWindow.appendChild(bubbleDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    // Text-to-speech for bot
    if (sender === 'bot' && 'speechSynthesis' in window) {
        const utter = new window.SpeechSynthesisUtterance(text);
        utter.lang = 'en-US';
        window.speechSynthesis.speak(utter);
    }
}

function clearChat() {
    chatWindow.innerHTML = '';
}

function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    appendMessage('patient', text);
    chatInput.value = '';
    appendMessage('bot', 'Processing...');
    axios.post('/get_advice', {text: text})
        .then(res => {
            // Remove last 'Processing...' message
            const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
            if (lastBotMsg) lastBotMsg.remove();
            appendMessage('bot', res.data.advice);
        })
        .catch(() => {
            const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
            if (lastBotMsg) lastBotMsg.remove();
            appendMessage('bot', 'Sorry, there was an error getting advice.');
        });
}

sendBtn.onclick = sendMessage;
chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') sendMessage();
});

// Push-to-talk (speech-to-text)
if (micBtn) {
    micBtn.onclick = function() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            appendMessage('bot', 'Speech recognition not supported in this browser.');
            return;
        }
        appendMessage('bot', 'Listening... Please speak now.');
        let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        recognition.onresult = function(event) {
            let transcript = event.results[0][0].transcript;
            appendMessage('patient', transcript);
            appendMessage('bot', 'Processing...');
            axios.post('/get_advice', {text: transcript})
                .then(res => {
                    const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
                    if (lastBotMsg) lastBotMsg.remove();
                    appendMessage('bot', res.data.advice);
                })
                .catch(() => {
                    const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
                    if (lastBotMsg) lastBotMsg.remove();
                    appendMessage('bot', 'Sorry, there was an error getting advice.');
                });
        };
        recognition.onerror = function() {
            appendMessage('bot', 'Speech recognition error.');
        };
        recognition.start();
    };
}

// Restart button
if (restartBtn) {
    restartBtn.onclick = function() {
        clearChat();
        appendMessage('bot', 'Hello! I am your ER assistant. Can you describe your symptoms?');
    };
}

// Go Back button
if (goBackBtn) {
    goBackBtn.onclick = function() {
        window.location.href = '/';
    };
}

// Initial greeting
window.addEventListener('DOMContentLoaded', function() {
    clearChat();
    appendMessage('bot', 'Hello! I am your ER assistant. Can you describe your symptoms?');
});
