from collections import namedtuple
import csv
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

ClassifiedData = namedtuple('ClassifiedData', 'PhraseId SentenceId Phrase Sentiment')
UnclassifiedData = namedtuple('UnclassifiedData', 'PhraseId SentenceId Phrase')


def read_tsv(filename, tuple_class):
    with open(filename, 'r') as f:
        # skip header
        next(f)
        for row in csv.reader(f, delimiter="\t"):
            yield tuple_class(*row)


def split_data_and_target(train_data):
    return [d.Phrase for d in train_data], [d.Sentiment for d in train_data]


train_data = list(read_tsv('train.tsv', ClassifiedData))
test_data = list(read_tsv('test.tsv', UnclassifiedData))
train_data_only, train_data_targets = split_data_and_target(train_data)


class Predictor(object):

    def __init__(self, feature_extractor=TfidfTransformer):
        self.classifier = MultinomialNB()
        self.feature_extractor = feature_extractor()

    def fit(self, X, y):
        X = self.feature_extractor.fit_transform(X, y)
        self.classifier.fit(X, y)

    def predict(self, X):
        X = self.feature_extractor.transform(X)
        return self.predict(X)


if __name__ == '__main__':
    print(len(train_data))
    print(len(test_data))
    print(len(train_data_only))
    print(len(train_data_targets))
    predictor = Predictor()
    predictor.fit(train_data_only, train_data_targets)
    #print(predictor.predict(test_data))
