__author__ = 'terrex'

from pfcsamr.orchestrator import *

import logging
logger = logging.getLogger(__name__)

from nose.tools import eq_


def test_step_1():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train.tsv")
    eq_(len(orchestrator.train_samples), 1999)

def test_step_2():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train.tsv")
    eq_(len(orchestrator.train_samples), 1999)
    orchestrator.vectorize()
    print(orchestrator.train_samples[0])

def test_step_3():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train.tsv")
    eq_(len(orchestrator.train_samples), 1999)
    orchestrator.vectorize()
    print(orchestrator.train_samples[0])
    orchestrator.stemmize()
    print(orchestrator.train_samples[0])

def test_step_4():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv("train.tsv")
    eq_(len(orchestrator.train_samples), 1999)
    orchestrator.vectorize()
    print(orchestrator.train_samples[0])
    orchestrator.stemmize()
    print(orchestrator.train_samples[0])
    orchestrator.lemmatize()
    print(orchestrator.train_samples[0])

