__author__ = 'terrex'

from nltk.stem import PorterStemmer, WordNetLemmatizer
from .types import TrainSample
__all__ = ('Filter', 'Stemmer', 'Lemmatizer', 'Vectorizer')


class Filter(object):

    def convert(self, train_sample):
        raise NotImplementedError()


class Vectorizer(Filter):

    def convert(self, train_sample):
        train_sample.phrase = train_sample.phrase.split()


# \cite{Perkins2010}
class Stemmer(Filter):

    def __init__(self):
        super(Stemmer, self).__init__()
        self._stemmer = PorterStemmer()

    def convert(self, train_sample):
        train_sample.phrase = [self._stemmer.stem(word) for word in train_sample.phrase]
        return train_sample


# \cite{Perkins2010}
class Lemmatizer(Filter):

    def __init__(self):
        super(Lemmatizer, self).__init__()
        self._lemmatizer = WordNetLemmatizer()

    def convert(self, train_sample):
        train_sample.phrase = [self._lemmatizer.lemmatize(word) for word in train_sample.phrase]
        return train_sample
