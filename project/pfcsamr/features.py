__author__ = 'terrex'

#from word2vec...

__all__ = ('bag_of_words_features',)


def bag_of_words_features(words):
    return {word: True for word in words}
