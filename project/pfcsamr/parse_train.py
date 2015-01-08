__author__ = 'terrex'

import csv
import pickle

from pfcsamr.types import Sample

__all__ = ['TrainParser', 'parse_train_and_save', 'read_saved_samples']


class TrainParser(object):

    def __init__(self, filename):
        self.filename = filename
        self.samples = []

    def parse(self):
        with open(self.filename, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            first = next(rdr)
            for row in rdr:
                words = row[2].split(r'\s+')
                sample = Sample(words=words, category=int(row[3]))
                self.samples.append(sample)

        return self.samples


def parse_train_and_save(tsv, dump):
    tp = TrainParser(tsv)
    pickle.dump(tp.parse(), open(dump, 'wb'))
    return tp.samples


def read_saved_samples(dump):
    return pickle.load(open(dump, 'rb'))
