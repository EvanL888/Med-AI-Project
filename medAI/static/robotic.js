// Robotic UI, Scan, and Speech-to-Text logic
let scanBtn = document.getElementById('scan-btn');
let beginBtn = document.getElementById('begin-btn');
let robotContainer = document.querySelector('.robot-container');
let robotFace = document.querySelector('.robot-face');
let homeBtn = document.getElementById('home-btn');
let scanBeam = document.getElementById('scan-beam');
let adviceBox = document.getElementById('advice-box');
let robotMouth = document.getElementById('robot-mouth');
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

// Speech-to-text and Azure AI advice
beginBtn.onclick = function() {
    adviceBox.style.display = 'block';
    adviceBox.textContent = 'Listening... Please describe your injury.';
    robotMouth.style.background = 'linear-gradient(90deg, #ff006e 60%, #23234a 100%)';
    // Move robot face to top left
    robotContainer.style.transition = 'none';
    robotContainer.style.position = 'fixed';
    robotContainer.style.top = '24px';
    robotContainer.style.left = '24px';
    robotContainer.style.transform = 'none';
    robotContainer.style.width = '180px';
    robotContainer.style.height = '180px';
    robotFace.classList.add('robot-top-left');
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        adviceBox.textContent = 'Speech recognition not supported in this browser.';
        robotMouth.style.background = '';
        return;
    }
    let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;
        adviceBox.textContent = 'Processing...';
        robotMouth.style.background = '';
        axios.post('/get_advice', {text: transcript})
            .then(res => {
                adviceBox.textContent = res.data.advice;
                // Text-to-speech: read the advice aloud
                if ('speechSynthesis' in window) {
                    let utter = new window.SpeechSynthesisUtterance(res.data.advice);
                    utter.lang = 'en-US';
                    utter.rate = 1.0;
                    window.speechSynthesis.speak(utter);
                }
            })
            .catch(() => {
                adviceBox.textContent = 'Error getting advice.';
            });
    };
    recognition.onerror = function() {
        adviceBox.textContent = 'Could not recognize speech.';
        robotMouth.style.background = '';
    };
    recognition.onend = function() {
        robotMouth.style.background = '';
    };
    recognition.start();
};
