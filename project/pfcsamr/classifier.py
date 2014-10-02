import pickle
from pfcsamr.readers import bag_of_words

if __name__ == '__main__':
    nb_classifier = None
    with open('nb_classifier.pickle', 'rb') as f:
        nb_classifier = pickle.load(f)
    skip_first_line = False
    with open('test.tsv', 'r') as f:
        print("PhraseId,Sentiment")
        for line in f:
            if not skip_first_line:
                skip_first_line = True
                continue

            line = line.strip()
            try:
                phrase_id, sentence_id, words = line.split('\t')
                words = words.split(' ')
                bow = bag_of_words(words)
                category = nb_classifier.classify(bow)
                print(phrase_id, ',', category, sep='')
            except ValueError:
                # there is no words
                phrase_id, sentence_id = line.split('\t')
                print(phrase_id, ',', 2, sep='')
                pass