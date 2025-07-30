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
const speechToggleBtn = document.getElementById('speech-toggle-btn');

// Conversation history for consultation
let conversationHistory = [];
let currentPatient = null;
let isReturningPatient = false;

// SVGs for icons
// Stylized robot face SVG (modern, friendly)
const botSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 48 48" fill="none"><rect width="48" height="48" rx="24" fill="#4f8cff"/><ellipse cx="24" cy="28" rx="12" ry="8" fill="#fff"/><ellipse cx="17.5" cy="21.5" rx="3.5" ry="4.5" fill="#fff"/><ellipse cx="30.5" cy="21.5" rx="3.5" ry="4.5" fill="#fff"/><ellipse cx="17.5" cy="22" rx="1.5" ry="2" fill="#23234a"/><ellipse cx="30.5" cy="22" rx="1.5" ry="2" fill="#23234a"/><rect x="20" y="32" width="8" height="2" rx="1" fill="#23234a"/></svg>`;
// Neutral human avatar SVG (friendly silhouette)
const patientSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 48 48" fill="none"><rect width="48" height="48" rx="24" fill="#43a047"/><ellipse cx="24" cy="20" rx="8" ry="8" fill="#fff"/><ellipse cx="24" cy="36" rx="14" ry="8" fill="#fff" fill-opacity="0.85"/></svg>`;

// Configuration for auto-speech
let autoSpeechEnabled = true; // Default to enabled for voice interaction
let currentAudio = null; // Track current playing audio

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

    // Add speaker and stop icons for bot messages to indicate TTS capability
    if (sender === 'bot') {
        const audioControlsDiv = document.createElement('div');
        audioControlsDiv.style.display = 'inline-block';
        audioControlsDiv.style.marginLeft = '5px';

        const speakerIcon = document.createElement('span');
        speakerIcon.innerHTML = '🔊';
        speakerIcon.style.cursor = 'pointer';
        speakerIcon.style.fontSize = '14px';
        speakerIcon.style.marginRight = '5px';
        speakerIcon.title = 'Click to hear this message';
        speakerIcon.onclick = () => speakText(text);

        const stopIcon = document.createElement('span');
        stopIcon.innerHTML = '⏹️';
        stopIcon.style.cursor = 'pointer';
        stopIcon.style.fontSize = '14px';
        stopIcon.title = 'Stop audio playback';
        stopIcon.onclick = () => stopAudio();

        audioControlsDiv.appendChild(speakerIcon);
        audioControlsDiv.appendChild(stopIcon);
        contentDiv.appendChild(audioControlsDiv);
    }

    bubbleDiv.appendChild(iconDiv);
    bubbleDiv.appendChild(contentDiv);
    chatWindow.appendChild(bubbleDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Add to conversation history
    conversationHistory.push({
        role: sender === 'bot' ? 'assistant' : 'user',
        content: text
    });

    // Enhanced text-to-speech for bot messages using Azure TTS
    if (sender === 'bot' && autoSpeechEnabled) {
        // Use Azure TTS with a small delay to avoid overwhelming the user
        setTimeout(() => {
            speakText(text);
        }, 300);
    }
}

function clearChat() {
    chatWindow.innerHTML = '';
    conversationHistory = [];
    currentPatient = null;
    isReturningPatient = false;
}

// Helper function to extract patient name from conversation
function extractPatientName(history) {
    for (let msg of history) {
        if (msg.role === 'user') {
            const content = msg.content.toLowerCase();
            // Look for name patterns
            const namePatterns = [
                /my name is\s+([a-zA-Z\s]+)/i,
                /i am\s+([a-zA-Z\s]+)/i,
                /this is\s+([a-zA-Z\s]+)/i
            ];

            for (let pattern of namePatterns) {
                const match = content.match(pattern);
                if (match && match[1].trim().split(' ').length >= 2) {
                    return match[1].trim();
                }
            }

            // If first user message and looks like a name
            if (history.indexOf(msg) <= 2 && /^[a-zA-Z\s]+$/.test(msg.content) && msg.content.trim().split(' ').length >= 2) {
                return msg.content.trim();
            }
        }
    }
    return null;
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

            // Check if an existing patient was found
            if (res.data.existing_patient && res.data.existing_patient.found) {
                currentPatient = res.data.existing_patient;
                isReturningPatient = true;

                // Show returning patient notification
                const welcomeMessage = `Welcome back, ${currentPatient.name}! I found your previous medical record from ${currentPatient.last_consultation}. Let me review your information and focus on any new concerns or updates since your last visit.`;
                appendMessage('bot', welcomeMessage);

                // Show patient summary
                if (currentPatient.summary) {
                    const summaryMessage = `Here's a summary of your existing information: ${currentPatient.summary}`;
                    appendMessage('bot', summaryMessage);
                }
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

// Text-to-Speech function using Azure TTS
function speakText(text) {
    // Stop any currently playing audio
    stopAudio();

    axios.post('/text-to-speech', { text: text })
        .then(response => {
            const audioBase64 = response.data.audio;
            if (audioBase64) {
                // Convert base64 to audio blob and play
                const audioBlob = base64ToBlob(audioBase64, 'audio/mpeg');
                const audioUrl = URL.createObjectURL(audioBlob);
                currentAudio = new Audio(audioUrl);

                // Add event listener to clean up when audio ends
                currentAudio.addEventListener('ended', () => {
                    currentAudio = null;
                    URL.revokeObjectURL(audioUrl);
                });

                // Add event listener to clean up on error
                currentAudio.addEventListener('error', () => {
                    currentAudio = null;
                    URL.revokeObjectURL(audioUrl);
                });

                currentAudio.play().catch(error => {
                    console.error('Error playing audio:', error);
                    currentAudio = null;
                    URL.revokeObjectURL(audioUrl);
                });
            }
        })
        .catch(error => {
            console.error('Text-to-speech error:', error);
            // Fallback to browser's built-in speech synthesis
            fallbackTextToSpeech(text);
        });
}

// Function to stop current audio playback
function stopAudio() {
    // Stop Azure TTS audio
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
        currentAudio = null;
    }

    // Stop browser's built-in speech synthesis
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
    }
}

// Helper function to convert base64 to blob
function base64ToBlob(base64, mimeType) {
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
}

// Fallback text-to-speech using browser's built-in synthesis
function fallbackTextToSpeech(text) {
    if ('speechSynthesis' in window) {
        // Stop any currently playing speech
        speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.8;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        speechSynthesis.speak(utterance);
    }
}

sendBtn.onclick = sendMessage;
chatInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') sendMessage();
});

// Push-to-talk (speech-to-text) - Enhanced with Azure Speech Services
if (micBtn) {
    let isRecording = false;
    let mediaRecorder;
    let audioChunks = [];

    micBtn.onclick = function () {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    };

    function startRecording() {
        // Check if browser supports media recording
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            appendMessage('bot', 'Voice recording not supported in this browser.');
            return;
        }

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                isRecording = true;
                micBtn.style.backgroundColor = '#ff4444';
                micBtn.innerHTML = '🛑'; // Stop icon
                appendMessage('bot', 'Recording... Click the microphone again to stop.');

                audioChunks = [];
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    sendAudioToServer(audioBlob);

                    // Reset UI
                    micBtn.style.backgroundColor = '';
                    micBtn.innerHTML = '🎤';
                    isRecording = false;

                    // Stop all tracks to release the microphone
                    stream.getTracks().forEach(track => track.stop());
                };

                mediaRecorder.start();
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                appendMessage('bot', 'Could not access microphone. Please check permissions.');
            });
    }

    function stopRecording() {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
        }
    }

    function sendAudioToServer(audioBlob) {
        appendMessage('bot', 'Processing your voice...');

        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.wav');

        axios.post('/speech-to-text', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
            .then(response => {
                const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
                if (lastBotMsg) {
                    lastBotMsg.remove();
                    conversationHistory.pop(); // Remove "Processing..." from history
                }

                const transcription = response.data.transcription;
                if (transcription) {
                    appendMessage('patient', transcription);

                    // Now send the transcribed text to the consultation chat
                    sendMessageToConsultation(transcription);
                } else {
                    appendMessage('bot', 'Could not understand your speech. Please try again or type your response.');
                }
            })
            .catch(error => {
                console.error('Speech-to-text error:', error);
                const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
                if (lastBotMsg) {
                    lastBotMsg.remove();
                    conversationHistory.pop();
                }
                appendMessage('bot', 'Sorry, there was an error processing your speech. Please try typing instead.');
            });
    }

    // Fallback to browser's built-in speech recognition if Azure fails
    function fallbackSpeechRecognition() {
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
            sendMessageToConsultation(transcript);
        };
        recognition.onerror = function (event) {
            appendMessage('bot', 'Speech recognition error. Please try typing your response.');
        };
        recognition.start();
    }
}

// Helper function to send message to consultation endpoint
function sendMessageToConsultation(message) {
    appendMessage('bot', 'Processing...');

    // Use consultation_chat endpoint for structured consultation
    axios.post('/consultation_chat', {
        message: message,
        history: conversationHistory.slice(0, -2) // Exclude the current user message and "Processing..." message
    })
        .then(res => {
            const lastBotMsg = chatWindow.querySelector('.er-bubble.bot:last-child');
            if (lastBotMsg) {
                lastBotMsg.remove();
                conversationHistory.pop(); // Remove "Processing..." from history
            }

            // Check if an existing patient was found
            if (res.data.existing_patient && res.data.existing_patient.found) {
                currentPatient = res.data.existing_patient;
                isReturningPatient = true;

                // Show returning patient notification
                const welcomeMessage = `Welcome back, ${currentPatient.name}! I found your previous medical record from ${currentPatient.last_consultation}.`;
                appendMessage('bot', welcomeMessage);
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

// Restart button
if (restartBtn) {
    restartBtn.onclick = function () {
        clearChat();
        appendMessage('bot', 'Welcome to your comprehensive medical consultation! I\'m here to gather detailed information about your health, medical history, and current concerns. If you\'ve been here before, I can access your previous medical records to save time. This consultation will help create a complete medical record that can be shared with healthcare providers. Let\'s begin with your basic information: What is your full name?');
    };
}

// Generate Report button
if (generateReportBtn) {
    generateReportBtn.onclick = function () {
        if (conversationHistory.length < 10) {
            appendMessage('bot', 'I need more comprehensive information before generating a complete medical report. Please continue answering the consultation questions.');
            return;
        }

        appendMessage('bot', 'Generating your comprehensive medical consultation report and saving your information...');

        // First save patient data to database
        const patientName = extractPatientName(conversationHistory);

        if (patientName) {
            // Save patient information
            axios.post('/save_patient', {
                name: patientName,
                history: conversationHistory.slice(0, -1)
            })
                .then(() => {
                    console.log('Patient data saved successfully');
                })
                .catch(err => {
                    console.error('Error saving patient data:', err);
                });
        }

        // Generate report
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

                // Store report data in sessionStorage for the report page
                sessionStorage.setItem('medicalReport', res.data.report);

                // Create report ready message with button to view report
                const reportBubble = document.createElement('div');
                reportBubble.className = 'er-bubble bot report-bubble';

                const iconDiv = document.createElement('div');
                iconDiv.className = 'er-bot-icon';
                iconDiv.innerHTML = botSVG;

                const contentDiv = document.createElement('div');
                contentDiv.className = 'er-bubble-content report-content';
                contentDiv.innerHTML = `
                    <h3>📋 Medical Report Generated Successfully!</h3>
                    <p>Your comprehensive medical consultation report has been prepared and is ready for review.</p>
                    <p><strong>Report includes:</strong></p>
                    <ul>
                        <li>Patient identification and contact information</li>
                        <li>Vital signs and measurements</li>
                        <li>Medical history and current medications</li>
                        <li>Lifestyle assessment</li>
                        <li>Clinical recommendations</li>
                        <li>Medical records authorization status</li>
                    </ul>
                    <p>Click the button below to view your detailed medical report in a professional format.</p>
                `;

                // Add view report button
                const viewReportBtn = document.createElement('button');
                viewReportBtn.textContent = '📋 View Medical Report';
                viewReportBtn.className = 'view-report-btn';
                viewReportBtn.style.cssText = `
                    background: linear-gradient(135deg, #3182ce, #2c5282);
                    color: white;
                    border: none;
                    padding: 15px 25px;
                    border-radius: 8px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    cursor: pointer;
                    margin: 15px 10px 5px 0;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3);
                `;
                viewReportBtn.onmouseover = function () {
                    this.style.background = 'linear-gradient(135deg, #2c5282, #2a4365)';
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 6px 16px rgba(49, 130, 206, 0.4)';
                };
                viewReportBtn.onmouseout = function () {
                    this.style.background = 'linear-gradient(135deg, #3182ce, #2c5282)';
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 4px 12px rgba(49, 130, 206, 0.3)';
                };
                viewReportBtn.onclick = function () {
                    window.open('/medical_report', '_blank');
                };

                // Add download button for backup
                const downloadBtn = document.createElement('button');
                downloadBtn.textContent = '💾 Download Backup';
                downloadBtn.className = 'download-report-btn';
                downloadBtn.onclick = function () {
                    downloadReport(res.data.report);
                };

                contentDiv.appendChild(viewReportBtn);
                contentDiv.appendChild(downloadBtn);
                reportBubble.appendChild(iconDiv);
                reportBubble.appendChild(contentDiv);
                chatWindow.appendChild(reportBubble);
                chatWindow.scrollTop = chatWindow.scrollHeight;
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

// Speech Toggle button
if (speechToggleBtn) {
    speechToggleBtn.onclick = function () {
        autoSpeechEnabled = !autoSpeechEnabled;
        speechToggleBtn.textContent = autoSpeechEnabled ? '🔊 Auto-Speech: ON' : '🔇 Auto-Speech: OFF';
        speechToggleBtn.title = autoSpeechEnabled ? 'Click to disable automatic speech' : 'Click to enable automatic speech';

        // Stop any currently playing speech
        if (!autoSpeechEnabled && 'speechSynthesis' in window) {
            speechSynthesis.cancel();
        }

        // Visual feedback
        speechToggleBtn.style.backgroundColor = autoSpeechEnabled ? '#4caf50' : '#f44336';
        setTimeout(() => {
            speechToggleBtn.style.backgroundColor = '';
        }, 200);
    };
}

// Initial greeting
window.addEventListener('DOMContentLoaded', function () {
    // Only show consultation greeting if we're on the consultation page
    if (chatWindow) {
        clearChat();
        const welcomeMessage = 'Welcome to your comprehensive medical consultation! I\'m here to gather detailed information about your health, medical history, and current concerns. If you\'ve been here before, I can access your previous medical records to save time. This consultation will help create a complete medical record that can be shared with healthcare providers. Let\'s begin with your basic information: What is your full name?';

        appendMessage('bot', welcomeMessage);

        // Automatically speak the welcome message
        setTimeout(() => {
            speakText(welcomeMessage);
        }, 500); // Small delay to ensure the message is displayed first
    }
});
