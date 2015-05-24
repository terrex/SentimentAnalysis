__author__ = 'terrex'

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
# from word2vec...
from .mytypes import TrainSample

from .trainers import load_wordbin

import numpy as np

__all__ = ('bag_of_words_features', 'Bower', 'BowerBiGram', 'Word2Vec')


def bag_of_words_features(words):
    return {word: True for word in words}


def vectorized_features(words, trained_corpus):
    pass


# #
# # extract word features for each category
# #           >>> trained_model['woman']
# #          array([ -1.40128313e-02, ...]
# # then train with scikit-learn 5X dimensional features.


class FeatureExtractorI(object):
    def extract_feats(self, train_sample: TrainSample) -> TrainSample:
        raise NotImplementedError()


# \cite{Perkins2010}
def bag_of_words(words):
    return {word: True for word in words}


def bag_of_bigrams_words(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(words + bigrams)


class Bower(FeatureExtractorI):
    def extract_feats(self, train_sample: TrainSample) -> TrainSample:
        train_sample.feats = bag_of_words(train_sample.words)
        return train_sample


class BowerBiGram(FeatureExtractorI):
    def extract_feats(self, train_sample: TrainSample) -> TrainSample:
        train_sample.feats = bag_of_bigrams_words(train_sample.words)
        return train_sample


class Word2Vec(FeatureExtractorI):
    def extract_feats(self, train_sample: TrainSample) -> TrainSample:
        model = load_wordbin()
        feat_word2vec = np.ones_like(model.vectors[0])
        for word in train_sample.words:
            try:
                wordvec = model.get_vector(word)
                feat_word2vec = feat_word2vec * wordvec
            except KeyError:
                pass

        train_sample.feats = {'vec': feat_word2vec}
        return train_sample
