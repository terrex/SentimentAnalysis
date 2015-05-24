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
    load_wordbin()