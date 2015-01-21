__author__ = 'terrex'

import csv
import pickle
import re

from pfcsamr.types import Sample

__all__ = ('Parser', 'TrainParser', 'TestParser',
           'parse_and_save_samples', 'read_saved_samples')


class Parser(object):

    def __init__(self, filename):
        self.filename = filename
        self.samples = []

    def parse(self):
        raise NotImplementedError()


class TrainParser(Parser):

    def parse(self):
        with open(self.filename, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            first = next(rdr)
            for row in rdr:
                words = re.split(r'\s+', row[2])
                sample = Sample(words=words, category=int(row[3]))
                self.samples.append(sample)

        return self.samples


class TestParser(Parser):

    def parse(self):
        with open(self.filename, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            first = next(rdr)
            for row in rdr:
                words = re.split(r'\s+', row[2])
                sample = Sample(words=words, category=None)
                self.samples.append(sample)

        return self.samples


def parse_and_save_samples(tsv, dump, parser_class=TrainParser):
    tp = parser_class(tsv)
    pickle.dump(tp.parse(), open(dump, 'wb'))
    return tp.samples


def read_saved_samples(dump):
    return pickle.load(open(dump, 'rb'))
