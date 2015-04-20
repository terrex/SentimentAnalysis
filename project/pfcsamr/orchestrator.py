__author__ = 'terrex'

import csv

from .features import *
from .types import *
from .filters import *


class Orchestrator(object):
    def __init__(self):
        self.file_path = None
        """:type: str"""
        self.train_samples = []
        """:type: list[TrainSample]"""

    def open_train_tsv(self, file_path=None):
        self.file_path = file_path
        with open(file_path, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            first = next(rdr)
            for row in rdr:
                train_sample = TrainSample(*row)
                self.train_samples.append(train_sample)

        return self

    def vectorize(self):
        vectorizer = Vectorizer()
        for sample in self.train_samples:
            vectorizer.convert(sample)
        return self

    def remove_stopwords(self):
        stopwords_remover = StopwordsRemover()
        for sample in self.train_samples:
            stopwords_remover.convert(sample)
        return self

    def stemmize(self):
        stemmer = Stemmer()
        for sample in self.train_samples:
            stemmer.convert(sample)
        return self

    def lemmatize(self):
        lemmatizer = Lemmatizer()
        for sample in self.train_samples:
            lemmatizer.convert(sample)
        return self

    def bow(self):
        bower = Bower()
        for sample in self.train_samples:
            bower.extract_feats(sample)
        return self

    def bow_bigrams(self):
        bower_bigram = BowerBiGram()
        for sample in self.train_samples:
            bower_bigram.extract_feats(sample)
        return self
