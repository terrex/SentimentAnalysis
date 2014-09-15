"""
0,2076
1,4670
2,4643
3,4943
4,2353
total: 18685
"""

import random


if __name__ == '__main__':
    categories = []
    categories += [0] * 2076
    categories += [1] * 4670
    categories += [2] * 4643
    categories += [3] * 4943
    categories += [4] * 2353
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
                category = random.choice(categories)
                print(phrase_id, ',', category, sep='')
            except ValueError:
                # there is no words
                phrase_id, sentence_id = line.split('\t')
                print(phrase_id, ',', 2, sep='')
                pass
