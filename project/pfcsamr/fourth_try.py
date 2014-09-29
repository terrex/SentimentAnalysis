from collections import namedtuple
import csv
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import cross_val_score, KFold
from sklearn import metrics
from scipy.stats import sem
import numpy as np
import concurrent.futures

ClassifiedData = namedtuple('ClassifiedData', 'PhraseId SentenceId Phrase Sentiment')
UnclassifiedData = namedtuple('UnclassifiedData', 'PhraseId SentenceId Phrase')


def read_tsv(filename, tuple_class):
    with open(filename, 'r') as f:
        # skip header
        next(f)
        for row in csv.reader(f, delimiter="\t"):
            yield tuple_class(*row)


def data2targets(samples):
    return [sample.Sentiment for sample in samples]


train_data = list(read_tsv('train.tsv', ClassifiedData))
test_data = list(read_tsv('test.tsv', UnclassifiedData))


def evaluate_cross_validation(clf, X, y, K):
    cv = KFold(len(y), K, shuffle=True)
    scores = cross_val_score(clf, X, y, cv=cv)
    return np.mean(scores)


class PhraseExtractor(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit_transform(self, X, y=None, **fit_params):
        return [sample.Phrase for sample in X]

    def fit(self, X, y=None):
        self.labels_ = [sample.Sentiment for sample in X]
        return self

    def transform(self, X, y=None):
        return [sample.Phrase for sample in X]


class TreeOfPairsVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.labels_ = []
        self.phrases_ = []

    def fit(self, X, y=None):
        self.labels_ = y
        self.phrases_ = np.array([[1] for phrase in X], np.float64)
        return self.phrases_

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y=y)
        return self.transform(X, y=y)

    def transform(self, X, y=None):
        return self.phrases_


def testargs(**kwargs):
    print("Process started")
    classifier = make_pipeline(
        PhraseExtractor(),
        TreeOfPairsVectorizer(),
        MultinomialNB(),
    )
    score = evaluate_cross_validation(classifier, train_data[:100], data2targets(train_data[:100]), 5)
    return "mean score: {}".format(score)


if __name__ == '__main__':
    print(len(train_data))
    print(len(test_data))
    print(testargs())
