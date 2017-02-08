from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import models
import random

def scramble(s):
    return "".join(random.sample(s, len(s)))

@models.db_session
def check_pronounceability(word):
    words = [w.strip() for w in open('words.txt') if w == w.lower()]
    scrambled = [scramble(w) for w in words]

    X = words+scrambled
    y = ['word']*len(words) + ['unpronounceable']*len(scrambled)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    text_clf = Pipeline([
        ('vect', CountVectorizer(analyzer='char', ngram_range=(1, 3))),
        ('clf', MultinomialNB())
        ])
    text_clf = text_clf.fit(X_train, y_train)
    stuff = text_clf.predict_proba([word])
    pronounceability = round(100*stuff[0][1], 2)
    models.Word(pronounceability=pronounceability)
    models.commit()
    return pronounceability
