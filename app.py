import random
def scramble(s):
    return "".join(random.sample(s, len(s)))

words = [w.strip() for w in open('/usr/share/dict/words') if w == w.lower()]
scrambled = [scramble(w) for w in words]

X = words+scrambled
y = ['word']*len(words) + ['unpronounceable']*len(scrambled)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

text_clf = Pipeline([
    ('vect', CountVectorizer(analyzer='char', ngram_range=(1, 3))),
    ('clf', MultinomialNB())
    ])

text_clf = text_clf.fit(X_train, y_train)
predicted = text_clf.predict(X_test)

from sklearn import metrics
print(metrics.classification_report(y_test, predicted))

print(text_clf.predict("hola how are you lou".split()))