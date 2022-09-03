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

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        nfn_model = tf.keras.models.load_model('model/nfn_model.h5')
        data = request.args.get('message')

        if data is None:
            return jsonify({
                "error": "Invalid data"
            })

        # preprocess text
        data = data.lower()
        data = data.replace('https://', ' ')
        data = re.sub('[^a-zA-Z0-9 ]', ' ', data)
        data = " ".join(data.split())

        lemmatizer = WordNetLemmatizer()
        data = ["".join([lemmatizer.lemmatize(word) for word in data])]

        ohe = [one_hot(text, 10000) for text in data]

        emb_doc = tf.keras.preprocessing.sequence.pad_sequences(
            ohe,
            maxlen=5292,
            padding="pre"
        )

        pred = nfn_model.predict(np.array(emb_doc))
        percentage = float(pred[0][0])

        verdict, certainty = "", 0

        if percentage > 0.8:
            verdict = "Fake"
        elif percentage > 0.6:
            verdict = "Likely Fake"
        elif percentage > 0.4:
            verdict = "Mixed"
        elif percentage > 0.2:
            verdict = "Likely Real"
        else:
            verdict = "Real"
    
    return jsonify({
        "verdict": verdict,
        "probability": percentage,
        "text": repr(data)
    })

if __name__ == '__main__':
    app.run(debug=True)