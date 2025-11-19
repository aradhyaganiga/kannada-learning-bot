// API Base URL
const API_URL = 'http://localhost:5000';

let currentKannadaText = '';

// Translation Function
async function translateText() {
    const input = document.getElementById('translateInput');
    const resultBox = document.getElementById('translationResult');
    const speakBtn = document.getElementById('speakBtn');
    
    const text = input.value.trim();
    
    if (!text) {
        resultBox.innerHTML = '<span style="color: #ff6b6b;">Please enter some text to translate.</span>';
        return;
    }
    
    resultBox.innerHTML = '<div class="loading"></div> Translating...';
    speakBtn.style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/translate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.kannada) {
            currentKannadaText = data.kannada;
            resultBox.innerHTML = `
                <div>
                    <strong>English:</strong> ${data.english}<br>
                    <strong style="font-size: 24px; color: #764ba2;">Kannada:</strong> 
                    <span style="font-size: 24px; color: #667eea;">${data.kannada}</span>
                </div>
            `;
            resultBox.classList.add('show');
            speakBtn.style.display = 'block';
        } else {
            resultBox.innerHTML = '<span style="color: #ff6b6b;">Translation not available.</span>';
        }
    } catch (error) {
        console.error('Translation error:', error);
        resultBox.innerHTML = '<span style="color: #ff6b6b;">Error connecting to server. Make sure Flask is running!</span>';
    }
}

// Text-to-Speech Function
function speakKannada() {
    if (!currentKannadaText) {
        alert('No Kannada text to speak!');
        return;
    }
    
    // Using Web Speech API
    const utterance = new SpeechSynthesisUtterance(currentKannadaText);
    utterance.lang = 'kn-IN'; // Kannada language code
    utterance.rate = 0.8; // Slightly slower for learning
    
    // Try to find Kannada voice
    const voices = speechSynthesis.getVoices();
    const kannadaVoice = voices.find(voice => voice.lang.includes('kn'));
    if (kannadaVoice) {
        utterance.voice = kannadaVoice;
    }
    
    speechSynthesis.speak(utterance);
}

// Load voices when they're available
speechSynthesis.onvoiceschanged = function() {
    speechSynthesis.getVoices();
};

// Chat Functions
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const chatContainer = document.getElementById('chatContainer');
    
    const message = input.value.trim();
    
    if (!message) {
        return;
    }
    
    // Display user message
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'chat-message user-message';
    userMessageDiv.innerHTML = `<strong>You:</strong> ${message}`;
    chatContainer.appendChild(userMessageDiv);
    
    input.value = '';
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot-message';
    typingDiv.innerHTML = '<strong>Bot:</strong> <div class="loading"></div>';
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        chatContainer.removeChild(typingDiv);
        
        // Display bot response
        const botMessageDiv = document.createElement('div');
        botMessageDiv.className = 'chat-message bot-message';
        botMessageDiv.innerHTML = `<strong>Bot:</strong> ${data.bot_response}`;
        chatContainer.appendChild(botMessageDiv);
        
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        // Optional: Speak the response
        const utterance = new SpeechSynthesisUtterance(data.bot_response);
        utterance.lang = 'kn-IN';
        utterance.rate = 0.8;
        speechSynthesis.speak(utterance);
        
    } catch (error) {
        console.error('Chat error:', error);
        chatContainer.removeChild(typingDiv);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'chat-message bot-message';
        errorDiv.innerHTML = '<strong>Bot:</strong> <span style="color: #ff6b6b;">Error connecting to server!</span>';
        chatContainer.appendChild(errorDiv);
    }
}

function handleChatEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Flashcards Functions
async function loadFlashcards() {
    const container = document.getElementById('flashcardsContainer');
    
    try {
        const response = await fetch(`${API_URL}/flashcards`);
        const data = await response.json();
        
        container.innerHTML = '';
        
        data.flashcards.forEach((card, index) => {
            const flashcardDiv = document.createElement('div');
            flashcardDiv.className = 'flashcard';
            flashcardDiv.innerHTML = `
                <div class="flashcard-content">${card.english}</div>
                <div class="flashcard-translation" style="display:none;">${card.kannada}</div>
                <div class="flashcard-pronunciation" style="display:none;">${card.pronunciation}</div>
            `;
            
            flashcardDiv.addEventListener('click', function() {
                this.classList.toggle('flipped');
                const translation = this.querySelector('.flashcard-translation');
                const pronunciation = this.querySelector('.flashcard-pronunciation');
                const content = this.querySelector('.flashcard-content');
                
                if (this.classList.contains('flipped')) {
                    content.textContent = card.kannada;
                    translation.style.display = 'block';
                    translation.textContent = card.english;
                    pronunciation.style.display = 'block';
                    
                    // Speak the Kannada word
                    const utterance = new SpeechSynthesisUtterance(card.kannada);
                    utterance.lang = 'kn-IN';
                    speechSynthesis.speak(utterance);
                } else {
                    content.textContent = card.english;
                    translation.style.display = 'none';
                    pronunciation.style.display = 'none';
                }
            });
            
            container.appendChild(flashcardDiv);
        });
        
    } catch (error) {
        console.error('Flashcards error:', error);
        container.innerHTML = '<p style="color: #ff6b6b;">Error loading flashcards. Make sure Flask is running!</p>';
    }
}

// Initialize flashcards on page load
window.addEventListener('load', function() {
    loadFlashcards();
});