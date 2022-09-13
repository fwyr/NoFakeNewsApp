from flask import Flask, render_template, url_for, request, jsonify

# import libraries for AI model
import numpy as np
import random
import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
stop_words = set(stopwords.words("english"))
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
 
import tensorflow as tf
import gensim
from tensorflow import keras
from keras_preprocessing.text import Tokenizer, tokenizer_from_json
from keras_preprocessing.sequence import pad_sequences

nfn_model = tf.keras.models.load_model('model/nfn_model_w2v.h5')

with open('model/nfn_tokenizer.json') as f:
    tokenizer_json = json.load(f)
    nfn_tokenizer = tokenizer_from_json(tokenizer_json)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        data = request.args.get('message')

        if data is None:
            return jsonify({
                "error": "Invalid data"
            })

        # preprocess text
        filtered = []
        data = nltk.sent_tokenize(data)
        for sentence in data:
            sentence = sentence.lower()
            tokens = tokenizer.tokenize(sentence)
            filtered_words = [w.strip() for w in tokens if w not in stop_words and len(w) > 1]
            filtered.extend(filtered_words)
        data = [filtered]
        data = nfn_tokenizer.texts_to_sequence(data)
        
        verdict, percentage = 0, 0
        
       # verdict, certainty = "", 0
       #if percentage > 0.8:
        #    verdict = "Fake"
       #elif percentage > 0.6:
       #     verdict = "Likely Fake"
        #elif percentage > 0.4:
       #     verdict = "Mixed"
       # elif percentage > 0.2:
       #     verdict = "Likely Real"
       # else:
        #    verdict = "Real"
    
    return jsonify({
        "verdict": verdict,
        "probability": percentage,
        "processed_text": repr(data)
    })

if __name__ == '__main__':
    app.run(debug=True)