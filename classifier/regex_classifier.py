import numpy as np
from copy import copy
from .base_classifier import BaseClassifier
from util.string_functions import split_string_into_sentences

class RegexClassifier(BaseClassifier):
    '''
    Class specialized in classifying patient data using regexes
    '''
    def __init__(self, classifier_name, regexes, data=None, labels=None, ids=None):
        '''
        Initializes RegexClassifier

        :param classifier_name: Name of classifier
        :param regexes: List of Regex objects
        :param data: List of data
        :param labels: List of labels
        :param ids: List of ids
        '''
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)
        self.regexes = regexes

    def weighted_score_text(self, text, regexes):
        pass

    def naive_score_text(self, text, regexes):
        '''
        Naively scores text by summing the match scores in the Regex objects

        :param text: A string of text
        :param regexes: A list of Regex objects

        :return: List of Regex Objects that matched with the text, total_score
        '''

        matches = []
        total_score = 0
        for regex in regexes:
            regex_copy = copy(regex)
            regex_copy.clear_matches()
            regex_matches = regex_copy.determine_matches(text)
            score = regex.score*len(regex_matches)

            if len(regex_matches) > 0:
                matches.append(regex_copy)

            total_score += score

        return matches, total_score

    def score_sentence(self, text, regexes, score_func=None):
        '''
        Given regexes, score_func and text, determines a score for the sentence using score_func

        :param text: String of text
        :param regexes: List of Regex objects
        :param score_func: function used for scoring sentence

        :return: A list of Regex Objects that matched and total score
        '''

        func = self.naive_score_text if score_func is None else score_func
        matches, total_score = func(text, regexes)

        return matches, total_score

    def score_sentences(self, text, regexes, score_func=None):
        '''
        Given regexes, score_func and text, determines a score for the sentence using score_func

        :param text: Text to be split into sentences
        :param regexes: List of Regex Objects to search for in each sentence
        :param score_func: function used for score each sentence

        :return: List of (list of Regex objects that matched,score) tuples and a total_score
        '''

        sentences = split_string_into_sentences(text)
        matches_score_list = []
        total_score = 0

        for sentence in sentences:
            matches, score = self.score_sentence(sentence, regexes)
            if matches:
                matches_score_list.append((matches, score))

            total_score += score

        return matches_score_list, total_score

    def run_classifier(self, score_func=None):
        print("\nRunning Classifier:", self.name)

        # full_text = " ".join(self.data)
        #
        # pos_indices = self.labels == 1
        # pos_data = self.data[pos_indices]
        # neg_data = self.data[~pos_indices]
        # pos_ids = self.data[pos_indices]
        # neg_ids = self.data[~pos_indices]
        #
        # pos_text = " ".join(pos_data)
        # neg_text = " ".join(neg_data)

        # self.score_text("This is text")

        for id, datum, label in zip(self.ids, self.data, self.labels):
            matches, score = self.score_sentences(datum, self.regexes)
            if matches:
                print(id, score, label)



