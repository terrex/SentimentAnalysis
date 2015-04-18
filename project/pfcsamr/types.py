__author__ = 'terrex'

from collections import namedtuple, defaultdict


__all__ = ('Sample', 'iter_samples_words', 'TrainSample')

Sample = namedtuple('Sample', ['words', 'category'])

def iter_samples_words(samples):
    return (sample.words for sample in samples)


def samples_to_categories_map(samples):
    result = defaultdict(list)

    for sample in samples:
        result[sample.category].append(sample)

    return result


TrainSampleNamedtuple = namedtuple('TrainSampleNamedtuple', ['phrase_id', 'sentence_id', 'phrase', 'sentiment'])


class TrainSample(TrainSampleNamedtuple):

    @TrainSampleNamedtuple.phrase_id.setter
    def _set_phrase_id(self, value):
        self._phrase_id = int(value)

    @TrainSampleNamedtuple.sentence_id.setter
    def _set_sentence_id(self, value):
        self._sentence_id = int(value)

    @TrainSampleNamedtuple.sentiment.setter
    def _set_sentiment(self, value):
        self._sentiment = int(value)
