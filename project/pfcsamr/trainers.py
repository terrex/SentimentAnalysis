__author__ = 'terrex'

import word2vec
from sklearn.datasets.base import Bunch

__all__ = ('load_wordbin',)


def load_wordbin():
    # TODO: word2vec.load('pfcsamr/GoogleNews-vectors-negative300.bin')
    return word2vec.load('pfcsamr/text8.bin')
