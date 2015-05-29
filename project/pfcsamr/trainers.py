__author__ = 'terrex'

import word2vec
from sklearn.datasets.base import Bunch
from gensim.models.word2vec import Word2Vec

__all__ = ('load_wordbin',)


def load_wordbin():
    # TODO: word2vec.load('pfcsamr/GoogleNews-vectors-negative300.bin')
    #model = Word2Vec.load_word2vec_format('pfcsamr/text8.bin', binary=True)
    #model = Word2Vec.load_word2vec_format('pfcsamr/GoogleNews-vectors-negative300.bin', binary=True)
    model = word2vec.load('pfcsamr/text8.bin')
    return model

