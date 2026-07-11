from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
import os

app = Flask(__name__)
CORS(app)

# Load model and vectorizer
MODEL_PATH = 'mlp_model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'

model = None
cv = None

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    print("Loading model and vectorizer...")
    model = joblib.load(MODEL_PATH)
    cv = joblib.load(VECTORIZER_PATH)
    
    # Ensure NLTK data is downloaded
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
else:
    print(f"WARNING: Model or vectorizer not found. Please run train.py first.")

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stop_words and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
        
    return " ".join(y)

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not cv:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 503
        
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
        
    text = data['text']
    
    try:
        # Preprocess
        transformed = transform_text(text)
        # Vectorize
        vectorized = cv.transform([transformed]).toarray()
        # Predict (0 = Not Spam, 1 = Spam based on our train script encoding)
        prediction = model.predict(vectorized)[0]
        
        result = "spam" if prediction == 1 else "not spam"
        
        return jsonify({
            'prediction': result,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use Render's PORT environment variable, or default to 5000 locally
    port = int(os.environ.get('PORT', 5000))
    # Host '0.0.0.0' is required for cloud deployments
    app.run(host='0.0.0.0', port=port, debug=False)
