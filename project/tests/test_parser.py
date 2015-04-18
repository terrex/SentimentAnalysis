__author__ = 'terrex'

import logging

from pfcsamr.parser import *

logger = logging.getLogger(__name__)

from nose.tools import eq_


def test_parse_and_save_and_read_samples_train():
    logger.debug("p&s&r train")
    saved = parse_and_save_samples('train.tsv', 'train_samples.pickle', TrainParser)
    read = read_saved_samples('train_samples.pickle')
    eq_(saved, read)


def test_parse_and_save_and_read_samples_test():
    logger.debug("p&s&r test")
    saved = parse_and_save_samples('test.tsv', 'test_samples.pickle', TestParser)
    read = read_saved_samples('test_samples.pickle')
    eq_(saved, read)
