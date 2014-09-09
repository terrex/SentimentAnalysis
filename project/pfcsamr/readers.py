from nltk.corpus import CategorizedCorpusReader, PlaintextCorpusReader
from nltk.corpus.reader.util import StreamBackedCorpusView


class SamrTsvView(StreamBackedCorpusView):
    def __init__(self, *args, **kwargs):
        kwargs['startpos'] = 1
        super().__init__(self, args[0], **kwargs)

    def read_block(self, stream):
        words = super().read_block(stream)
        phrase_id, sentence_id, phrase, sentiment = words[0], words[1], words[2:-1], words[-1]

class SamrParsedCorpusReader(PlaintextCorpusReader):
    CorpusView = SamrTsvView

class KaggleSamrReader(SamrParsedCorpusReader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

if __name__ == '__main__':
    ksr = KaggleSamrReader('..', 'train.tsv')
    ksr.sents()
