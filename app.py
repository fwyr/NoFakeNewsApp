from flask import Flask, render_template, url_for, request

# import libraries for AI model
import pandas as pd
import numpy as np

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
 
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dropout, Embedding, LSTM, Dense
from keras.models import Sequential
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
        data = [message]

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

        if percentage > 0.5:
            verdict = "Fake"
            certainty = f"{round(percentage * 100, 2)}%"
        else:
            verdict = "Real"
            certainty = f"{round(100 - percentage * 100, 2)}%"
        
    return render_template('result.html', verdict=verdict, certainty=certainty, prediction=pred)

if __name__ == '__main__':
    app.run(debug=True)
    