from flask import Flask, render_template, url_for, request, jsonify

# import modules
import io, json
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('punkt')
stop_words = set(stopwords.words("english"))
nltk_tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
import tensorflow as tf
import gensim
from tensorflow import keras
from keras_preprocessing.text import Tokenizer, tokenizer_from_json
from keras_preprocessing.sequence import pad_sequences

# load app
app = Flask(__name__)

# load model
nfn_model = tf.keras.models.load_model('model/nfn_model_w2v.h5')

# load tokenizer
with open('model/nfn_tokenizer.json') as f:
    tokenizer_json = json.load(f)
    nfn_tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_json)

# define app routes
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
            tokens = nltk_tokenizer.tokenize(sentence)
            filtered_words = [w.strip() for w in tokens if w not in stop_words and len(w) > 1]
            filtered.extend(filtered_words)
        data = nfn_tokenizer.texts_to_sequences([filtered])
        data = pad_sequences(data, maxlen=700)

        score = nfn_model.predict(data)[0][0]
        verdict = ""

        if score <= 0.2:
            verdict = "Real"
        elif score <= 0.4:
            verdict = "Likely Real"
        elif score <= 0.6:
            verdict = "Mixed"
        elif score <= 0.8:
            verdict = "Likely Fake"
        else:
            verdict = "Fake"

        return jsonify({
            "verdict": verdict,
            "score": str(score),
            "processed_text": repr(filtered)
        })

if __name__ == '__main__':
    app.run(debug=True)