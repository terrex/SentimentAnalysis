__author__ = 'terrex'

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

from pfcsamr.orchestrator import Orchestrator


def test_nb():
    orchestrator = Orchestrator()
    orchestrator.open_train_tsv('train.tsv')
    orchestrator.tokenize()
    orchestrator.remove_stopwords()
    orchestrator.stemmize()
    orchestrator.lemmatize()
    orchestrator.bow_bigrams()
    orchestrator.split_trainset(.75)
    orchestrator.learn_nb()
    sent = orchestrator.classify(orchestrator.train_samples[5])
    logger.debug("sent is %d".format(sent))
    f1 = orchestrator.learn_evaluate()
    logger.debug("F-score is %f".format(f1))
