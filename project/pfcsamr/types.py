__author__ = 'terrex'

from collections import namedtuple, defaultdict


__all__ = ('Sample', 'iter_samples_words')

Sample = namedtuple('Sample', ['words', 'category'])


def iter_samples_words(samples):
    return (sample.words for sample in samples)


def samples_to_categories_map(samples):
    result = defaultdict(list)

    for sample in samples:
        result[sample.category].append(sample)

    return result
