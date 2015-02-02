__author__ = 'terrex'

from pfcsamr.features import *

import logging
logger = logging.getLogger(__name__)

from nose.tools import eq_


def test_bag_of_words_features():
    logger.debug("Testing empty bow")
    features = bag_of_words_features([])
    should = {}
    eq_(features, should)

    logger.debug("Testing 4-words bow")
    features = bag_of_words_features(['one', 'word', 'another', 'third'])
    should = {'third': True, 'one': True, 'word': True, 'another': True}
    eq_(features, should)
