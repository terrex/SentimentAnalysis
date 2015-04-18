__author__ = 'terrex'

import csv

from .types import *
from .filters import *


class Orchestrator(object):
    def __init__(self):
        self.file_path = None
        self.train_samples = []

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
        self.train_samples = [vectorizer.convert(sample) for sample in self.train_samples]
        return self

    def remove_stopwords(self):
        stopwords_remover = StopwordsRemover()
        self.train_samples = [stopwords_remover.convert(sample) for sample in self.train_samples]
        return self

    def stemmize(self):
        stemmer = Stemmer()
        self.train_samples = [stemmer.convert(sample) for sample in self.train_samples]
        return self

    def lemmatize(self):
        lemmatizer = Lemmatizer()
        self.train_samples = [lemmatizer.convert(sample) for sample in self.train_samples]
        return self
