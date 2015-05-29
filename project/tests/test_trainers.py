__author__ = 'terrex'

import logging
import logging.config

from pfcsamr.trainers import load_wordbin


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

_multiprocess_can_split_ = False

import os

os.environ['PATH'] += ":/opt/local/libexec/word2vec"

def test_word2vec():
    import word2vec

    word2vec.word2phrase('pfcsamr/text8', 'pfcsamr/text8-phrases')
    word2vec.word2vec('pfcsamr/text8-phrases', 'pfcsamr/text8.bin', size=100, verbose=True)


def test_load_wordbin():
    print("kiyo ke")
    logger.debug("eyy")
    #load_wordbin()


def test_gensim():
    from gensim.models.word2vec import Word2Vec
    model_orig = Word2Vec.load_word2vec_format('pfcsamr/text8.bin', binary=True)
    model_orig.save('pfcsamr/text8.bin.gensim')
    model_new = Word2Vec.load('pfcsamr/text8.bin.gensim', mmap='r')
    print(model_new)

def test_gensim_load_mmap():
    from gensim.models.word2vec import Word2Vec
    model_new = Word2Vec.load('pfcsamr/GoogleNews-vectors-negative300.bin.gensim', mmap='r')
    print(model_new)
