from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simple English to Kannada translation dictionary
translation_dict = {
    'hello': 'ನಮಸ್ಕಾರ',
    'hi': 'ಹಾಯ್',
    'good morning': 'ಶುಭೋದಯ',
    'good night': 'ಶುಭ ರಾತ್ರಿ',
    'thank you': 'ಧನ್ಯವಾದ',
    'please': 'ದಯವಿಟ್ಟು',
    'yes': 'ಹೌದು',
    'no': 'ಇಲ್ಲ',
    'water': 'ನೀರು',
    'food': 'ಆಹಾರ',
    'book': 'ಪುಸ್ತಕ',
    'school': 'ಶಾಲೆ',
    'house': 'ಮನೆ',
    'friend': 'ಸ್ನೇಹಿತ',
    'family': 'ಕುಟುಂಬ',
    'mother': 'ತಾಯಿ',
    'father': 'ತಂದೆ',
    'brother': 'ಸಹೋದರ',
    'sister': 'ಸಹೋದರಿ',
    'love': 'ಪ್ರೀತಿ',
    'happy': 'ಸಂತೋಷ',
    'sad': 'ದುಃಖ',
    'beautiful': 'ಸುಂದರ',
    'good': 'ಒಳ್ಳೆಯದು',
    'bad': 'ಕೆಟ್ಟದು',
    'big': 'ದೊಡ್ಡ',
    'small': 'ಸಣ್ಣ',
    'hot': 'ಬಿಸಿ',
    'cold': 'ತಣ್ಣನೆಯ',
    'how are you': 'ನೀವು ಹೇಗಿದ್ದೀರಿ',
    'what is your name': 'ನಿಮ್ಮ ಹೆಸರೇನು',
    'my name is': 'ನನ್ನ ಹೆಸರು',
    'i am fine': 'ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ',
    'bye': 'ವಿದಾಯ',
    'welcome': 'ಸ್ವಾಗತ',
    'sorry': 'ಕ್ಷಮಿಸಿ',
    'help': 'ಸಹಾಯ',
    'teacher': 'ಶಿಕ್ಷಕ',
    'student': 'ವಿದ್ಯಾರ್ಥಿ',
    'today': 'ಇಂದು',
    'tomorrow': 'ನಾಳೆ',
    'yesterday': 'ನಿನ್ನೆ',
    'time': 'ಸಮಯ',
    'money': 'ಹಣ',
    'city': 'ನಗರ',
    'village': 'ಗ್ರಾಮ',
    'country': 'ದೇಶ',
    'india': 'ಭಾರತ',
    'language': 'ಭಾಷೆ',
    'kannada': 'ಕನ್ನಡ',
    'english': 'ಇಂಗ್ಲಿಷ್',
    'one': 'ಒಂದು',
    'two': 'ಎರಡು',
    'three': 'ಮೂರು',
    'four': 'ನಾಲ್ಕು',
    'five': 'ಐದು',
    'can you help me?': 'ನೀನು ನನಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆಯಾ? (Neenu nanage sahaaya maadaballeya?)',
    'where is the hotel?': 'ಹೋಟೆಲ್ ಎಲ್ಲಿದೆ? (Hotel ellide?)',
    'what time is it?': 'ಈಗ ಎಷ್ಟು ಗಂಟೆ? (Eega eshtu gante?)',
    'i am thirsty': 'ನನಗೆ ಬಾಯಾರಿಕೆ ಆಗಿದೆ (Nanage baayaarike aagide)',
    'call the police': 'ಪೋಲಿಸರಿಗೆ ಕರೆ ಮಾಡಿ (Polisarige kare maadi)',
    'nice to meet you': 'ನಿಮ್ಮನ್ನು ಭೇಟಿಯಾದುದು ಸಂತೋಷ (Nimmannu bhetiyaadudu santosha)',
    'what do you do?': 'ನೀನು ಏನು ಮಾಡ್ತೀಯ? (Neenu enu maadtīya?)'

}

# Chatbot responses
chatbot_responses = {
    'hello': 'ನಮಸ್ಕಾರ! ನಾನು ಕನ್ನಡ ಕಲಿಕೆ ಬೋಟ್. ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?',
    'hi': 'ಹಾಯ್! ನಾನು ನಿಮಗೆ ಕನ್ನಡ ಕಲಿಸಲು ಇಲ್ಲಿದ್ದೇನೆ.',
    'how are you': 'ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ, ಧನ್ಯವಾದ! ನೀವು ಹೇಗಿದ್ದೀರಿ?',
    'what is your name': 'ನನ್ನ ಹೆಸರು ಕನ್ನಡ ಬೋಟ್. ನಿಮ್ಮ ಹೆಸರೇನು?',
    'teach me kannada': 'ಖಂಡಿತ! ನಾನು ನಿಮಗೆ ಕನ್ನಡ ಪದಗಳು ಮತ್ತು ವಾಕ್ಯಗಳನ್ನು ಕಲಿಸುತ್ತೇನೆ.',
    'thank you': 'ನಿಮಗೆ ಸ್ವಾಗತ! ಕಲಿಯುವುದನ್ನು ಮುಂದುವರಿಸಿ!',
    'bye': 'ವಿದಾಯ! ಶೀಘ್ರದಲ್ಲಿ ಮತ್ತೆ ಮಾತನಾಡೋಣ!',
    'help': 'ನಾನು ನಿಮಗೆ ಇಂಗ್ಲಿಷ್ ಪದಗಳನ್ನು ಕನ್ನಡಕ್ಕೆ ಅನುವಾದಿಸಲು ಸಹಾಯ ಮಾಡಬಲ್ಲೆ!',
    'good morning': 'ಶುಭೋದಯ! ಇಂದು ಒಳ್ಳೆಯ ದಿನವಾಗಲಿ!',
    'good night': 'ಶುಭ ರಾತ್ರಿ! ಚೆನ್ನಾಗಿ ಮಲಗಿ!',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    english_text = data.get('text', '').lower().strip()
    
    if not english_text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Try exact match first
    if english_text in translation_dict:
        return jsonify({
            'english': data.get('text'),
            'kannada': translation_dict[english_text]
        })
    
    # Try word by word translation
    words = english_text.split()
    translated_words = []
    for word in words:
        translated_words.append(translation_dict.get(word, word))
    
    kannada_text = ' '.join(translated_words)
    
    return jsonify({
        'english': data.get('text'),
        'kannada': kannada_text
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower().strip()
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Find best matching response
    response = 'ಕ್ಷಮಿಸಿ, ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ.'
    
    for key, value in chatbot_responses.items():
        if key in user_message:
            response = value
            break
    
    return jsonify({
        'user_message': data.get('message'),
        'bot_response': response
    })

@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    flashcards = [
        {'english': 'Hello', 'kannada': 'ನಮಸ್ಕಾರ', 'pronunciation': 'Namaskara'},
        {'english': 'Thank you', 'kannada': 'ಧನ್ಯವಾದ', 'pronunciation': 'Dhanyavada'},
        {'english': 'Water', 'kannada': 'ನೀರು', 'pronunciation': 'Neeru'},
        {'english': 'Food', 'kannada': 'ಆಹಾರ', 'pronunciation': 'Aahara'},
        {'english': 'Friend', 'kannada': 'ಸ್ನೇಹಿತ', 'pronunciation': 'Snehita'},
        {'english': 'Mother', 'kannada': 'ತಾಯಿ', 'pronunciation': 'Taayi'},
        {'english': 'Father', 'kannada': 'ತಂದೆ', 'pronunciation': 'Tande'},
        {'english': 'Good Morning', 'kannada': 'ಶುಭೋದಯ', 'pronunciation': 'Shubhodaya'},
        {'english': 'Good Night', 'kannada': 'ಶುಭ ರಾತ್ರಿ', 'pronunciation': 'Shubha Raatri'},
        {'english': 'Beautiful', 'kannada': 'ಸುಂದರ', 'pronunciation': 'Sundara'},
        {'english': 'Love', 'kannada': 'ಪ್ರೀತಿ', 'pronunciation': 'Preeti'},
        {'english': 'Happy', 'kannada': 'ಸಂತೋಷ', 'pronunciation': 'Santosha'},
    ]
    return jsonify({'flashcards': flashcards})

if __name__ == '__main__':
    app.run(debug=True, port=5000)