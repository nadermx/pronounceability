from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import models
import random

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

@models.db_session
def check_pronounceability(word):
    stuff = text_clf.predict_proba([word])
    pronounceability = round(100*stuff[0][1], 2)
    models.Word(word=word, pronounceability=pronounceability)
    models.commit()
    return pronounceability