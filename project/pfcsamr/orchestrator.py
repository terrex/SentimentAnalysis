__author__ = 'terrex'

import csv
import logging
import logging.config

from .features import *
from .mytypes import *
from .filters import *


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


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

        logger.debug("Read %d train samples".format(len(self.train_samples)))
        return self

    def vectorize(self):
        vectorizer = Vectorizer()
        for sample in self.train_samples:
            vectorizer.convert(sample)

        logger.debug("%d train samples vectorized".format(len(self.train_samples)))
        return self

    def remove_stopwords(self):
        stopwords_remover = StopwordsRemover()
        for sample in self.train_samples:
            stopwords_remover.convert(sample)

        logger.debug("%d train samples cleaned out of stopwords".format(len(self.train_samples)))
        return self

    def stemmize(self):
        stemmer = Stemmer()
        for sample in self.train_samples:
            stemmer.convert(sample)

        logger.debug("%d train samples stemmed".format(len(self.train_samples)))
        return self

    def lemmatize(self):
        lemmatizer = Lemmatizer()
        for sample in self.train_samples:
            lemmatizer.convert(sample)

        logger.debug("%d train samples lemmed".format(len(self.train_samples)))
        return self

    def bow(self):
        bower = Bower()
        for sample in self.train_samples:
            bower.extract_feats(sample)

        logger.debug("%d train samples featured with BOW".format(len(self.train_samples)))
        return self

    def bow_bigrams(self):
        bower_bigram = BowerBiGram()
        for sample in self.train_samples:
            bower_bigram.extract_feats(sample)

        logger.debug("%d train samples featured with 2-BOW".format(len(self.train_samples)))
        return self

    def word2vec(self):
        word2vec = Word2Vec()
        for sample in self.train_samples:
            word2vec.extract_feats(sample)

        logger.debug("%d train samples featured with Word2Vec".format(len(self.train_samples)))
        return self
