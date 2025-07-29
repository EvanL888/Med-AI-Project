// --- Scan Button Animation ---
window.addEventListener('DOMContentLoaded', function () {
    const scanBtn = document.getElementById('scan-btn');
    const scanBeam = document.getElementById('scan-beam');
    const beginBtn = document.getElementById('begin-btn');

    if (scanBtn && scanBeam) {
        scanBtn.onclick = function () {
            scanBeam.style.opacity = '1';
            scanBeam.style.height = '100vh';
            setTimeout(function () {
                scanBeam.style.opacity = '0';
                scanBeam.style.height = '0';
            }, 1200);
        };
    }

    // Begin button navigation
    if (beginBtn) {
        beginBtn.onclick = function () {
            window.location.href = '/consultation';
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
const generateReportBtn = document.getElementById('generate-report-btn');

// Conversation history for consultation
let conversationHistory = [];

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

    // Add to conversation history
    conversationHistory.push({
        role: sender === 'bot' ? 'assistant' : 'user',
        content: text
    });

    // Text-to-speech for bot
    if (sender === 'bot' && 'speechSynthesis' in window) {
        const utter = new window.SpeechSynthesisUtterance(text);
        utter.lang = 'en-US';
        window.speechSynthesis.speak(utter);
    }
}

function clearChat() {
    chatWindow.innerHTML = '';
    conversationHistory = [];
}

function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    appendMessage('patient', text);
    chatInput.value = '';
    appendMessage('bot', 'Processing...');

    // Use consultation_chat endpoint for structured consultation
    axios.post('/consultation_chat', {
        message: text,
        history: conversationHistory.slice(0, -2) // Exclude the current user message and "Processing..." message
    })
        .then(res => {
            // Remove last 'Processing...' message
            const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
            if (lastBotMsg) {
                lastBotMsg.remove();
                conversationHistory.pop(); // Remove "Processing..." from history
            }
            appendMessage('bot', res.data.response);
        })
        .catch(() => {
            const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
            if (lastBotMsg) {
                lastBotMsg.remove();
                conversationHistory.pop(); // Remove "Processing..." from history
            }
            appendMessage('bot', 'Sorry, there was an error getting advice.');
        });
}

sendBtn.onclick = sendMessage;
chatInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') sendMessage();
});

// Push-to-talk (speech-to-text)
if (micBtn) {
    micBtn.onclick = function () {
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
        recognition.onresult = function (event) {
            let transcript = event.results[0][0].transcript;
            appendMessage('patient', transcript);
            appendMessage('bot', 'Processing...');

            // Use consultation_chat endpoint for structured consultation
            axios.post('/consultation_chat', {
                message: transcript,
                history: conversationHistory.slice(0, -2) // Exclude the current user message and "Processing..." message
            })
                .then(res => {
                    const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
                    if (lastBotMsg) {
                        lastBotMsg.remove();
                        conversationHistory.pop(); // Remove "Processing..." from history
                    }
                    appendMessage('bot', res.data.response);
                })
                .catch(() => {
                    const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
                    if (lastBotMsg) {
                        lastBotMsg.remove();
                        conversationHistory.pop(); // Remove "Processing..." from history
                    }
                    appendMessage('bot', 'Sorry, there was an error getting advice.');
                });
        };
        recognition.onerror = function () {
            appendMessage('bot', 'Speech recognition error.');
        };
        recognition.start();
    };
}

// Restart button
if (restartBtn) {
    restartBtn.onclick = function () {
        clearChat();
        appendMessage('bot', 'Hello! I\'m your medical consultation assistant. I\'ll ask you a series of questions to better understand your health concerns and provide you with a comprehensive report. Let\'s start: What is your main health concern or symptom today?');
    };
}

// Generate Report button
if (generateReportBtn) {
    generateReportBtn.onclick = function () {
        if (conversationHistory.length < 6) {
            appendMessage('bot', 'I need more information before generating a report. Please answer a few more questions about your health concerns.');
            return;
        }

        appendMessage('bot', 'Generating your medical consultation report...');

        axios.post('/generate_report', {
            history: conversationHistory.slice(0, -1) // Exclude the "Generating..." message
        })
            .then(res => {
                // Remove last 'Generating...' message
                const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
                if (lastBotMsg) {
                    lastBotMsg.remove();
                    conversationHistory.pop(); // Remove "Generating..." from history
                }

                // Create a special report bubble
                const reportBubble = document.createElement('div');
                reportBubble.className = 'er-bubble bot report-bubble';

                const iconDiv = document.createElement('div');
                iconDiv.className = 'er-bot-icon';
                iconDiv.innerHTML = botSVG;

                const contentDiv = document.createElement('div');
                contentDiv.className = 'er-bubble-content report-content';
                contentDiv.innerHTML = res.data.report.replace(/\n/g, '<br>');

                reportBubble.appendChild(iconDiv);
                reportBubble.appendChild(contentDiv);
                chatWindow.appendChild(reportBubble);
                chatWindow.scrollTop = chatWindow.scrollHeight;

                // Add download button for the report
                const downloadBtn = document.createElement('button');
                downloadBtn.textContent = 'Download Report';
                downloadBtn.className = 'download-report-btn';
                downloadBtn.onclick = function () {
                    downloadReport(res.data.report);
                };
                contentDiv.appendChild(downloadBtn);
            })
            .catch(() => {
                const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
                if (lastBotMsg) {
                    lastBotMsg.remove();
                    conversationHistory.pop(); // Remove "Generating..." from history
                }
                appendMessage('bot', 'Sorry, there was an error generating the report. Please try again.');
            });
    };
}

// Function to download report as text file
function downloadReport(reportText) {
    const blob = new Blob([reportText], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `medical_consultation_report_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Go Back button
if (goBackBtn) {
    goBackBtn.onclick = function () {
        window.location.href = '/';
    };
}

// Initial greeting
window.addEventListener('DOMContentLoaded', function () {
    // Only show consultation greeting if we're on the consultation page
    if (chatWindow) {
        clearChat();
        appendMessage('bot', 'Hello! I\'m your medical consultation assistant. I\'ll ask you a series of questions to better understand your health concerns and provide you with a comprehensive report. Let\'s start: What is your main health concern or symptom today?');
    }
});
