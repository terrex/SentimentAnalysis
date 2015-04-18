__author__ = 'terrex'

# from word2vec...

__all__ = ('bag_of_words_features',)


def bag_of_words_features(words):
    return {word: True for word in words}


def vectorized_features(words, trained_corpus):
    pass


    ##

    ## extract word features for each category
    ##           >>> trained_model['woman']
    ##          array([ -1.40128313e-02, ...]

    ## then train with scikit-learn 5X dimensional features.