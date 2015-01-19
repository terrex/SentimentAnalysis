__author__ = 'terrex'

from pfcsamr.parser import *


def test_parse_and_save_and_read_samples_train():
    saved = parse_and_save_samples('train.tsv', 'train_samples.pickle', TrainParser)
    read = read_saved_samples('train_samples.pickle')
    assert saved == read


def test_parse_and_save_and_read_samples_test():
    saved = parse_and_save_samples('test.tsv', 'test_samples.pickle', TestParser)
    read = read_saved_samples('test_samples.pickle')
    assert saved == read
