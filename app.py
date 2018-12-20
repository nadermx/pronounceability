from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelBinarizer
import random

app = Flask(__name__)

words = [w.strip() for w in open('words.txt') if w == w.lower()]
def scramble(s):
    return "".join(random.sample(s, len(s)))

scrambled = [scramble(w) for w in words]
X = words+scrambled
# explicitly create binary labels
label_binarizer = LabelBinarizer()
y = label_binarizer.fit_transform(['word']*len(words) + ['unpronounceable']*len(scrambled))

text_clf = Pipeline([
    ('vect', CountVectorizer(analyzer='char', ngram_range=(1, 3))),
    ('clf', MultinomialNB())
])
text_clf = text_clf.fit(X, y)
# you might want to persist the Pipeline to disk at this point to ensure it's not lost in case there is a crash

def check_pronounceability(word):
    stuff = text_clf.predict_proba([word])
    pronounceability = round(100*stuff[0][1], 2)
    return pronounceability


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/word', methods=['POST', 'GET'])
def check():
    if request.method == "POST":
        word = request.form.get('word', False)
        pronounceability = check_pronounceability(word)
        if not pronounceability:
            pronounceability = "0.0"
        return render_template('index.html', pronounceability=pronounceability)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug = True, threaded=True)
    app.run()

