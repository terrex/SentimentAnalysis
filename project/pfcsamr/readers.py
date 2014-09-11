from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
import pickle


class KaggleSamrReader(CategorizedPlaintextCorpusReader):
    pass


def bag_of_words(words, stopfile='english'):
    return {word: True for word in (set(words) - set(stopwords.words(stopfile))) if len(word) > 2}


if __name__ == '__main__':
    ksr = KaggleSamrReader('..', r'train_\d\.txt', cat_pattern=r'train_(\d)\.txt')
    feats = []
    for category in ksr.categories():
        for sent in ksr.sents(categories=(category,)):
            feats += [(bag_of_words(sent), category)]

    nb_classifier = NaiveBayesClassifier.train(feats)
    with open('nb_classifier.pickle', 'wb+') as f:
        pickle.dump(nb_classifier, f)
