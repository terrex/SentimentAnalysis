__author__ = 'terrex'

import logging
import logging.config

from pfcsamr.orchestrator import *


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

from nose.tools import eq_

_multiprocess_can_split_ = False

orchestrator = None
""":type: Orchestrator"""


def test_step_1():
    global orchestrator
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train_first100.tsv")
    eq_(len(orchestrator.train_samples), 100)


def test_step_2():
    global orchestrator
    orchestrator.tokenize()
    logger.debug(orchestrator.train_samples[0])


def test_step_3():
    global orchestrator
    orchestrator.remove_stopwords()
    logger.debug(orchestrator.train_samples[0])


def test_step_4():
    global orchestrator
    orchestrator.stemmize()
    logger.debug(orchestrator.train_samples[0])


def test_step_5():
    global orchestrator
    orchestrator.lemmatize()
    logger.debug(orchestrator.train_samples[0])


def test_step_6a():
    global orchestrator
    orchestrator.bow()
    logger.debug(orchestrator.train_samples[0])


def test_step_6b():
    global orchestrator
    orchestrator.bow_bigrams()
    logger.debug(orchestrator.train_samples[0])


def test_step_6c():
    global orchestrator
    orchestrator.word2vec()
    logger.debug(orchestrator.train_samples[0])

def test_step_7():
    global orchestrator
    orchestrator.vectorize()
