from flask import Flask, render_template, url_for, request, jsonify

# import libraries for AI model
import numpy as np

import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
 
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import one_hot


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    nfn_model = tf.keras.models.load_model('model/nfn_model.h5')
    
    if request.method == 'POST':
        message = request.form['message']
        data = [message][0]

        # preprocess text
        data = data.lower()
        data = data.replace('https://', ' ')
        data = data.replace('http://', ' ')
        data = re.sub('[^a-zA-Z0-9 ]', ' ', data)
        data = " ".join(data.split())

        stop_words = set(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()

        filtered = []
        for word in data.split():
            if word not in stop_words:
                filtered.append(word)
        
        data = " ".join(filtered)
        data = ["".join([lemmatizer.lemmatize(word) for word in data])]

        one_hot_encoded = [one_hot(text, 10000) for text in data]
        m = max([len(text) for text in one_hot_encoded])

        emb_doc = tf.keras.preprocessing.sequence.pad_sequences(
            one_hot_encoded,
            maxlen=5069,
            padding="pre"
        )

        pred = nfn_model.predict(np.array(emb_doc))
        percentage = float(pred[0][0])

        verdict, certainty = 0, 0

        if percentage > 0.75:
            verdict = "Fake"
            certainty = f"{round(percentage * 100, 2)}%"
        elif percentage > 0.5:
            verdict = "Potentially Fake"
        elif percentage > 0.25:
            verdict = "Potentially Real"
        else:
            verdict = "Real"
            certainty = f"{round(100 - percentage * 100, 2)}%"
        
    return jsonify({
        "verdict": verdict,
        "certainty": certainty,
        "prediction": percentage,
        "processed_text": repr(data)
    })

if __name__ == '__main__':
    app.run(debug=True)
    