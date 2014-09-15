from pfcsamr.readers import KaggleSamrReader


if __name__ == '__main__':
    ksr = KaggleSamrReader('.', r'train_\d\.txt', cat_pattern=r'train_(\d)\.txt')
    feats = []
    total = 0
    for category in ksr.categories():
        how_much = len(ksr.sents(categories=(category,)))
        total += how_much
        print(category, ',', how_much, sep='')

    print('total:', total)
