__author__ = 'terrex'

from .types import iter_samples_words
from gensim.models import Word2Vec

import re
import os

__all__ = ('generate_model_word2vec', 'load_word2vec_models')


def generate_model_word2vec(samples, *args, **kwargs):
    """Pending description

    :param samples: list of Sample tuples
    :param args: None
    :param kwargs: See Word2Vec():
        size=100, alpha=0.025, window=5, min_count=5,
        sample=0, seed=1, workers=1, min_alpha=0.0001, sg=1, hs=1, negative=0,
        cbow_mean=0, hashfxn=hash, iter=1
    :return:
    """
    kwargs.update(sentences=iter_samples_words(samples))
    return Word2Vec(**kwargs)


def save_word2vec_models(models, directory='.', pattern=r'word2vec_model_{}'):
    for category in models:
        models[category].save(os.path.join(directory, pattern.format(category)))


def load_word2vec_models(directory='.', pattern=r'word2vec_model_(\d+)'):
    result = dict()

    for filename in os.listdir(directory):
        match = re.match(pattern, filename)
        if match:
            dict[int(match.group(1))] = Word2Vec.load(match.group(0))

    return result
