from nltk.tree import Tree
from nltk.draw import draw_trees
import csv
from collections import namedtuple
from stat_parser import Parser as StatParser, display_tree
from nltk.classify import NaiveBayesClassifier


the_parser = StatParser()


def neutralize_tag(tag_str):
    return int(tag_str) - 2


Sample = namedtuple('Sample', ['tag', 'tree', 'words', 'features'])


def row_to_sample(row):
    return Sample(tag=neutralize_tag(row[3]), tree=the_parser.parse(row[2]), words=row[2].split(' '), features=dict())


class TrainParser(object):

    def __init__(self, filename):
        self.filename = filename
        self.samples = []
        self.classifier = None

    def parse(self):
        with open(self.filename, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            next(rdr)   # ignore header
            for row in rdr:
                print("Processing ", row)
                try:
                    self.samples.append(row_to_sample(row))
                except:
                    print("Exception raised processing row ", row)

                if len(self.samples) > 100:
                    break

        return self.samples

    def augment_feature_set(self):
        for i, sample in enumerate(self.samples):
            for subtree in sample.tree.subtrees():
                sample.features[repr(subtree)] = True

        return self.samples

    def learn(self):
        labeled_featuresets = [(sample.features, sample.tag) for sample in self.samples]
        self.classifier = NaiveBayesClassifier.train(labeled_featuresets=labeled_featuresets)
        return self.classifier.labels()

    def predict(self, features):
        return self.classifier.classify(features)

if __name__ == '__main__':
    tp = TrainParser('train.tsv')
    print(tp.parse())
    print(tp.augment_feature_set()[7])
    print(tp.learn())
    print(tp.samples[7])
    print(tp.predict(tp.samples[7].features))
