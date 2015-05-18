__author__ = 'terrex'

from collections import namedtuple, defaultdict
from types import SimpleNamespace

__all__ = ('Sample', 'iter_samples_words', 'TrainSample')


Sample = namedtuple('Sample', ['words', 'category'])


def iter_samples_words(samples):
    return (sample.words for sample in samples)


def samples_to_categories_map(samples):
    result = defaultdict(list)

    for sample in samples:
        result[sample.category].append(sample)

    return result


class TrainSample(SimpleNamespace):
    def __init__(self, phrase_id: int=None, sentence_id: int=None, phrase: str=None, sentiment: int=None):
        super(TrainSample, self).__init__()
        self._phrase_id = phrase_id
        self._sentence_id = sentence_id
        self._phrase = phrase
        self._sentiment = sentiment

        # more atts
        self._words = []
        self._feats = {}

    @property
    def phrase_id(self) -> int:
        return self._phrase_id

    @phrase_id.setter
    def phrase_id(self, value):
        self._phrase_id = int(value)

    @property
    def sentence_id(self) -> int:
        return self._sentence_id

    @sentence_id.setter
    def sentence_id(self, value):
        self._sentence_id = int(value)

    @property
    def phrase(self) -> str:
        return self._phrase

    @phrase.setter
    def phrase(self, value):
        self._phrase = value

    @property
    def sentiment(self):
        return self._sentiment

    @sentiment.setter
    def sentiment(self, value):
        self._sentiment = int(value)

    @property
    def words(self) -> list:
        return self._words

    @words.setter
    def words(self, value: list):
        self._words = value

    @property
    def feats(self) -> set:
        return self._feats

    @feats.setter
    def feats(self, value: dict):
        self._feats = value
