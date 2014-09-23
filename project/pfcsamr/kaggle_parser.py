from collections import namedtuple
from nltk.corpus import stopwords
from nltk.draw import tree
from nltk.parse import MaltParser
from nltk import pos_tag
import csv
from stat_parser import Parser

Sample = namedtuple('Sample', ['words', 'category'])


class TrainParser(object):

    def __init__(self, filename, use_stopwords=False):
        self.filename = filename
        self._use_stopwords = use_stopwords
        self.population = None

    def parse(self):
        stpwrds = set(stopwords.words('english'))
        population = []
        trees = []
        with open(self.filename, 'rt') as file:
            rdr = csv.reader(file, dialect='excel-tab')
            first = next(rdr)
            sentence_id = None
            for row in rdr:
                if sentence_id:
                    if row[1] != sentence_id:
                        break
                else:
                    sentence_id = row[1]

                wds = row[2].split(r'\s+')

                if self._use_stopwords:
                    wds = [w for w in wds if w not in stpwrds]

                sample = Sample(words=wds, category=int(row[3]))
                population.append(sample)
                parser = Parser()
                the_tree = parser.nltk_parse(" ".join(sample.words))
                trees.append(the_tree)

        tree.draw_trees(*trees)
        self.population = population
        return population


if __name__ == '__main__':
    tp = TrainParser('train.tsv', False)
    print(tp.parse())
