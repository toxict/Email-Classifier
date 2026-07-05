import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

print("Downloading required NLTK data...")
nltk.download('punkt')
nltk.download('stopwords')

print("Loading dataset...")
csv_path = "C:/Users/tejas/Downloads/spamandnotspam/spam.csv"
if not os.path.exists(csv_path):
    print(f"ERROR: Dataset not found at {csv_path}")
    print("Please ensure the CSV file is located at the specified path.")
    exit(1)

df = pd.read_csv(csv_path, encoding='utf-8', encoding_errors='ignore')

print("Cleaning data...")
df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True, errors='ignore')
df.rename(columns={"v1": "target", "v2": "text"}, inplace=True)
df = df.drop_duplicates(keep='first')

lc = LabelEncoder()
df['target'] = lc.fit_transform(df['target'])

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

print("Preprocessing text data (this might take a minute)...")
df['transformed_text'] = df['text'].apply(transform_text)

print("Vectorizing text...")
cv = CountVectorizer()
X = cv.fit_transform(df['transformed_text']).toarray()
Y = df['target'].values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=42, test_size=0.2)

print("Training MLP Classifier...")
model = MLPClassifier(max_iter=1000, random_state=42)
model.fit(X_train, Y_train)

print("Saving model and vectorizer...")
joblib.dump(model, 'mlp_model.pkl')
joblib.dump(cv, 'vectorizer.pkl')

print("Training complete! Model and vectorizer saved successfully.")
