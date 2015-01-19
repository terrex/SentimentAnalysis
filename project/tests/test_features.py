__author__ = 'terrex'

from pfcsamr.features import *


def test_bag_of_words_features():
    features = bag_of_words_features(['one', 'word', 'another', 'third'])
    assert features == {'third': True, 'one': True, 'word': True, 'another': True}
    features = bag_of_words_features([])
    assert features == {}
