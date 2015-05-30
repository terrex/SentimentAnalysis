__author__ = 'terrex'

import csv
import logging
import logging.config
import collections

from sklearn.datasets.base import Bunch

from .features import *
from .mytypes import *
from .filters import *
from .vectorizers import *

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class Orchestrator(object):
    def __init__(self):
        self.file_path = None
        """:type: str"""
        self.train_samples = []
        """:type: list[TrainSample]"""
        self.vectorized_train_samples = Bunch()
        self.percent = .75

    def _get_train_samples_split_train(self):
        c = len(self.train_samples)
        m = int(c * self.percent)
        return self.train_samples[:m]

    def _get_train_samples_split_eval(self):
        c = len(self.train_samples)
        m = int(c * self.percent)
        return self.train_samples[m:]

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

    def tokenize(self):
        tokenizer = Tokenizer()
        for sample in self.train_samples:
            tokenizer.convert(sample)

        logger.debug("%d train samples tokenized".format(len(self.train_samples)))
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

    def vectorize(self):
        vectorizer = SkLearnVectorizer()
        self.vectorized_train_samples = vectorizer.vectorize(self.train_samples)

    def learn_nb(self):
        from nltk.classify import NaiveBayesClassifier
        train_feats = []
        for sample in self._get_train_samples_split_train():
            train_feats.append((sample.feats, sample.sentiment))
        nb_classifier = NaiveBayesClassifier.train(train_feats)
        self.classifier = nb_classifier

    def classify(self, sample: TrainSample):
        return self.classifier.classify(sample.feats)

    def split_trainset(self, percent : float):
        self.percent = percent

    def learn_evaluate(self):
        from nltk.metrics import f_measure
        classified = []
        # from \citep{Perkins2010}
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for sample in self._get_train_samples_split_eval():
            refsets[sample.sentiment].add(frozenset(sample.feats))
            sample.guessed = self.classifier.classify(sample.feats)
            testsets[sample.guessed].add(frozenset(sample.feats))

        f1_scores = {}
        for category in refsets.keys():
            f1_scores[category] = f_measure(refsets[category], testsets[category])

        return f1_scores

