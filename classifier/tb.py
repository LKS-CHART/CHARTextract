from .base_classifier import BaseClassifier
from ngram.base_ngram import *

class TB(BaseClassifier):
    '''
    Class specialized in classifying TB patient data
    '''
    def __init__(self, classifier_name="TB Classifier", data=None, labels=None, ids=None):
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)

    # def _read_data_from_folders(self, folders=None):
    #     if folders is None:
    #         folders = self.data_folders
    #
    #     for folder in folders:
    #         print(folder)

    def run_classifier(self):
        print("\nRunning Classifier:", self.name)

        #Just calculating some summary ngrams

        full_text = " ".join(self.data)
        unigram = Ngram(full_text, 1)
        bigram = Ngram(full_text, 2)
        trigram = Ngram(full_text, 3)

        for ngram in [unigram, bigram, trigram]:
            print(ngram.n)
            ngram.get_ngram_logistics()
            print(ngram.ngram_to_frequency)
