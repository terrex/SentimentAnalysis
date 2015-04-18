__author__ = 'terrex'

from pfcsamr.orchestrator import *

import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

from nose.tools import eq_


def disabled_test_step_1():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train.tsv")
    eq_(len(orchestrator.train_samples), 1999)

def disabled_test_step_2():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train.tsv")
    eq_(len(orchestrator.train_samples), 1999)
    orchestrator.vectorize()
    logger.debug(orchestrator.train_samples[0])

def disabled_test_step_3():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train.tsv")
    eq_(len(orchestrator.train_samples), 1999)
    orchestrator.vectorize()
    logger.debug(orchestrator.train_samples[0])
    orchestrator.stemmize()
    logger.debug(orchestrator.train_samples[0])

def disabled_test_step_4():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train.tsv")
    eq_(len(orchestrator.train_samples), 1999)
    orchestrator.vectorize()
    logger.debug(orchestrator.train_samples[0])
    orchestrator.stemmize()
    logger.debug(orchestrator.train_samples[0])
    orchestrator.lemmatize()
    logger.debug(orchestrator.train_samples[0])
