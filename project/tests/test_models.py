__author__ = 'terrex'

from pfcsamr.models import *

import logging
logger = logging.getLogger(__name__)


def test_generate_models_word2vec():
    from pfcsamr.parser import read_saved_samples
    from pfcsamr.types import samples_to_categories_map
    logger.info('reading samples from train_samples.pickle')
    samples = read_saved_samples('train_samples.pickle')
    samples_dict = samples_to_categories_map(samples)
    models = dict()
    for category in samples_dict:
        models[category] = generate_model_word2vec(samples_dict[category])
        models[category].save('word2vec_model_{}'.format(category))

    logger.debug(models)
