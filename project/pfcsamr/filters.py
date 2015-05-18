__author__ = 'terrex'

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

from .mytypes import TrainSample


__all__ = ('FilterI', 'Stemmer', 'Lemmatizer', 'Vectorizer', 'StopwordsRemover')


class FilterI(object):
    def convert(self, train_sample):
        raise NotImplementedError()


class Vectorizer(FilterI):
    def convert(self, train_sample: TrainSample) -> TrainSample:
        train_sample.words = train_sample.phrase.split()
        return train_sample


# \cite{Perkins2010}
class StopwordsRemover(FilterI):
    def __init__(self):
        super(StopwordsRemover, self).__init__()
        self._stopwords_set = set(stopwords.words('english'))

    def convert(self, train_sample: TrainSample) -> TrainSample:
        train_sample.words = [word for word in train_sample.words if word not in self._stopwords_set]
        return train_sample


# \cite{Perkins2010}
class Stemmer(FilterI):
    def __init__(self):
        super(Stemmer, self).__init__()
        self._stemmer = PorterStemmer()

    def convert(self, train_sample: TrainSample) -> TrainSample:
        train_sample.words = [self._stemmer.stem(word) for word in train_sample.words]
        return train_sample


# \cite{Perkins2010}
class Lemmatizer(FilterI):
    def __init__(self):
        super(Lemmatizer, self).__init__()
        self._lemmatizer = WordNetLemmatizer()

    def convert(self, train_sample: TrainSample) -> TrainSample:
        train_sample.words = [self._lemmatizer.lemmatize(word) for word in train_sample.words]
        return train_sample
