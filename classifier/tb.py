import numpy as np
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

        #Setting all positive examples to 1
        self.labels[self.labels == 'y'] = 1
        self.labels[self.labels == 'n'] = 0

        #Removing that one example which has value 10 in the labels
        self.labels = self.labels[:-1]
        self.data = self.data[:-1]
        self.ids = self.ids[:-1]

        self.labels = self.labels.astype(np.float)

        pos_indices = self.labels == 1
        pos_data = self.data[pos_indices]
        neg_data = self.data[~pos_indices]
        pos_ids = self.data[pos_indices]
        neg_ids = self.data[~pos_indices]

        pos_text = " ".join(pos_data)
        neg_text = " ".join(neg_data)

        print("Number of positive examples : {0}\n".format(len(pos_data)))
        print("Number of negative examples : {0}\n".format(len(neg_data)))

        pos_unigram = Ngram(pos_text, 1, name="pos_1_gram")
        pos_bigram  = Ngram(pos_text, 2, name="pos_2_gram")
        pos_trigram = Ngram(pos_text, 3, name="pos_3_gram")

        neg_unigram = Ngram(neg_text, 1, name="neg_1_gram")
        neg_bigram  = Ngram(neg_text, 2, name="neg_2_gram")
        neg_trigram = Ngram(neg_text, 3, name="neg_3_gram")

        unigram = Ngram(full_text, 1, name="1_gram")
        bigram  = Ngram(full_text, 2, name="2_gram")
        trigram = Ngram(full_text, 3, name="3_gram")

        #Information does not seem to be useful in distinct classification
        #Trigrams are somewhat promising
        for ngram in [pos_unigram, pos_bigram, pos_trigram, neg_unigram, neg_bigram, neg_trigram, unigram, bigram, trigram]:
            ngram.get_ngram_logistics()

        print("Positive: TOP {0} ngrams".format(20))
        for ngram in [pos_unigram, pos_bigram, pos_trigram]:
            print(ngram.top_k_ngrams(10))

        print("\nNegative: TOP {0} ngrams".format(10))
        for ngram in [neg_unigram, neg_bigram, neg_trigram]:
            print(ngram.top_k_ngrams(10))

        print("\nTrigram: Intersection between positive and negative examples: \n", pos_trigram & neg_trigram)
        print("\nBigram: Intersection between positive and negative examples: \n", pos_bigram & neg_bigram)

        # print(set((pos_trigram & neg_trigram).keys()) == set((neg_trigram & pos_trigram).keys()))

        #Keys that appear in pos_trigram but not in neg_trigram
        print("\nPos trigram exclusive keys: ")
        pos_keys = set(pos_trigram.ngram_to_frequency.keys()) - set(neg_trigram.ngram_to_frequency.keys())
        print(pos_trigram.get_frequencies(list(pos_keys)))

        #Keys that appear in pos unigram but not in neg unigram
        print("\nPos unigram exclusive keys: ")
        pos_keys = set(pos_unigram.ngram_to_frequency.keys()) - set(neg_unigram.ngram_to_frequency.keys())
        print(pos_unigram.get_frequencies(list(pos_keys)))
