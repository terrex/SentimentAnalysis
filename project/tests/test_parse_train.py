__author__ = 'terrex'

from pfcsamr.parse_train import *


_saved = None
_read = None


def test_parse_train_and_save():
    global _saved
    _saved = parse_train_and_save('train.tsv', 'train_samples.pickle')


def test_read_saved_samples():
    global _read
    _read = read_saved_samples('train_samples.pickle')


def test_saved_and_read_are_the_same():
    global _saved, _read
    assert _saved == _read
