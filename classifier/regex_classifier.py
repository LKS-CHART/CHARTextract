import numpy as np
from .base_classifier import BaseClassifier
from ngram.base_ngram import *
from ngram.ngram_functions import get_unique_keys

class RegexClassifier(BaseClassifier):
    '''
    Class specialized in classifying patient data using regexes
    '''
    def __init__(self, classifier_name, regexes, data=None, labels=None, ids=None):
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)
        self.regexes = regexes

    # def _read_data_from_folders(self, folders=None):
    #     if folders is None:
    #         folders = self.data_folders
    #
    #     for folder in folders:
    #         print(folder)

    def weighted_score_text(self, text, regexes):
        pass

    def naive_score_text(self, text, regexes):
        '''
        Naively scores text by summing the match scores in the Regex objects

        :param text: A string of text
        :param regexes: A list of Regex objects

        :return: List of matches for each regex, total_score
        '''

        # for regex in regexes:
        pass

    def score_sentences(self, text, regexes, score_func):
        pass

    def score_sentence(self, text, regexes, score_func=None):
        func = self.naive_score_text if score_func is None else score_func
        matches, total_score = func(text, regexes)

    def run_classifier(self):
        print("\nRunning Classifier:", self.name)

        #Just calculating some summary ngrams
        full_text = " ".join(self.data)

        pos_indices = self.labels == 1
        pos_data = self.data[pos_indices]
        neg_data = self.data[~pos_indices]
        pos_ids = self.data[pos_indices]
        neg_ids = self.data[~pos_indices]

        pos_text = " ".join(pos_data)
        neg_text = " ".join(neg_data)

        # self.score_text("This is text")



