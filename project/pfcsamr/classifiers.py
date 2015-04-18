__author__ = 'terrex'


def classify_word2vec(models, sample):
    for category in models:
        model = models[category]
        """:type : Word2Vec"""
        model.syn0norm