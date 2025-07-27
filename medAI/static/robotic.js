// Microphone push-to-talk logic for consultation page
const micBtn = document.getElementById('mic-btn');
if (micBtn && chatWindow) {
    micBtn.onclick = function() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            appendMessage('bot', 'Speech recognition not supported in this browser.');
            return;
        }
        appendMessage('bot', 'Listening... Please speak now.');
        robotMouth.style.background = 'linear-gradient(90deg, #ff006e 60%, #23234a 100%)';
        let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        recognition.onresult = function(event) {
            let transcript = event.results[0][0].transcript;
            appendMessage('user', transcript);
            appendMessage('bot', 'Processing...');
            robotMouth.style.background = '';
            axios.post('/get_advice', {text: transcript})
                .then(res => {
                    // Remove last 'Processing...' message
                    const lastBotMsg = chatWindow.querySelector('.chat-message.bot:last-child');
                    if (lastBotMsg) lastBotMsg.remove();
                    appendMessage('bot', res.data.advice);
                })
                .catch(() => {
                    const lastBotMsg = chatWindow.querySelector('.chat-message.bot:last-child');
                    if (lastBotMsg) lastBotMsg.remove();
                    appendMessage('bot', 'Sorry, there was an error getting advice.');
                });
        };
        recognition.onerror = function() {
            appendMessage('bot', 'Speech recognition error.');
            robotMouth.style.background = '';
        };
        recognition.onend = function() {
            robotMouth.style.background = '';
        };
        recognition.start();
    };
}
// Robotic UI, Scan, and Speech-to-Text logic
// --- Chatbot UI logic ---
const scanBtn = document.getElementById('scan-btn');
const beginBtn = document.getElementById('begin-btn');
const homeBtn = document.getElementById('home-btn');
const scanBeam = document.getElementById('scan-beam');
const robotContainer = document.querySelector('.robot-container');
const robotFace = document.querySelector('.robot-face');
const robotMouth = document.getElementById('robot-mouth');
const chatWindow = document.getElementById('chat-window');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const speakBtn = document.getElementById('speak-btn');
const clearBtn = document.getElementById('clear-btn');

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-message ' + sender;
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble';
    bubble.textContent = text;
    msgDiv.appendChild(bubble);
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function clearChat() {
    chatWindow.innerHTML = '';
}

// Home button: reloads the page to reset state
homeBtn.onclick = function() {
    window.location.href = '/';
};

// Scan animation
scanBtn.onclick = function() {
    scanBeam.style.opacity = 1;
    scanBeam.style.height = '0';
    scanBeam.style.transition = 'none';
    scanBeam.style.top = '0';
    setTimeout(() => {
        scanBeam.style.transition = 'height 1.2s linear';
        scanBeam.style.height = '100vh';
    }, 10);
    setTimeout(() => {
        scanBeam.style.opacity = 0;
        scanBeam.style.height = '0';
    }, 1300);
};

// Begin Consultation: focus input and move robot
beginBtn.onclick = function() {
    chatInput.focus();
    robotContainer.style.transition = 'none';
    robotContainer.style.position = 'fixed';
    robotContainer.style.top = '24px';
    robotContainer.style.left = '24px';
    robotContainer.style.transform = 'none';
    robotContainer.style.width = '180px';
    robotContainer.style.height = '180px';
    robotFace.classList.add('robot-top-left');
    appendMessage('bot', 'Hello! Please describe your symptoms or ask a medical question. You can type or use the Speak button.');
};

// Send message (manual input)
function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    appendMessage('user', text);
    chatInput.value = '';
    appendMessage('bot', 'Processing...');
    axios.post('/get_advice', {text: text})
        .then(res => {
            // Remove last 'Processing...' message
            const lastBotMsg = chatWindow.querySelector('.chat-message.bot:last-child');
            if (lastBotMsg) lastBotMsg.remove();
            appendMessage('bot', res.data.advice);
        })
        .catch(() => {
            const lastBotMsg = chatWindow.querySelector('.chat-message.bot:last-child');
            if (lastBotMsg) lastBotMsg.remove();
            appendMessage('bot', 'Sorry, there was an error getting advice.');
        });
}

sendBtn.onclick = sendMessage;
chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') sendMessage();
});

// Speak button (speech-to-text)
speakBtn.onclick = function() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        appendMessage('bot', 'Speech recognition not supported in this browser.');
        return;
    }
    appendMessage('bot', 'Listening... Please speak now.');
    robotMouth.style.background = 'linear-gradient(90deg, #ff006e 60%, #23234a 100%)';
    let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;
        appendMessage('user', transcript);
        appendMessage('bot', 'Processing...');
        robotMouth.style.background = '';
        axios.post('/get_advice', {text: transcript})
            .then(res => {
                // Remove last 'Processing...' message
                const lastBotMsg = chatWindow.querySelector('.chat-message.bot:last-child');
                if (lastBotMsg) lastBotMsg.remove();
                appendMessage('bot', res.data.advice);
            })
            .catch(() => {
                const lastBotMsg = chatWindow.querySelector('.chat-message.bot:last-child');
                if (lastBotMsg) lastBotMsg.remove();
                appendMessage('bot', 'Sorry, there was an error getting advice.');
            });
    };
    recognition.onerror = function() {
        appendMessage('bot', 'Speech recognition error.');
        robotMouth.style.background = '';
    };
    recognition.onend = function() {
        robotMouth.style.background = '';
    };
    recognition.start();
};

// Clear chat
clearBtn.onclick = clearChat;
