from nltk.classify import NaiveBayesClassifier
import pickle

if __name__ == '__main__':
    nb_classifier = None
    with open('nb_classifier.pickle', 'rb') as f:
        nb_classifier = pickle.load()
    with open('test.tsv', 'r') as f:
        f.readline()
