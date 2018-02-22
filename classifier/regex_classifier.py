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

            #creating a copy because we want new unique regex objects for each match
            #reusing old regex objects will cause previous matches to be replaced by new matches and this behaviour
            #may not transfer well to multiple use cases

            regex_copy = copy(regex)
            regex_copy.clear_matches()

            #determining matches and computing score
            regex_matches = regex_copy.determine_matches(text)
            score = regex.score*len(regex_matches)

            if len(regex_matches) > 0:
                #adding the new copied regex object to matches
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

        :return: {sentence_i: {'matches': [Regex Objects], 'score': sentence_score}} and a total_score
        '''

        sentences = split_string_into_sentences(text)
        matches_score_dict = {}
        total_score = 0

        for i, sentence in enumerate(sentences):
            matches, score = self.score_sentence(sentence, regexes)

            #only adding sentences that matched
            if matches:
                matches_score_dict[i] = {"matches": matches, "score": score}

            total_score += score

        return matches_score_dict, total_score

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
            print(matches)

        '''
        
        TODO: 
        
        
        Set required labels e.g Smoking = 0, Never Smoked = 1, Past Smoker = 2
        
        create dict_1 reg_name -> freq
        
        #Used only for vanilla frequency counting. Scale frequency method will use a different technique
        For each sentence compute regex frequencies
            dict[reg_name] += freq
        
        ??Scale Frequency based on sentence index?? 
            -Potential formula
            - sum((match_index(regex_match)/len_matches)*(sentence_index/num_sentences))
                -Effect: Later terms penalized less, more matches penalized less since (1+2+3...k)/k is divergent
        
        normalize_frequencies [Perhaps unneeded if using frequency scaling]
        
        train_svm method
            Classify data

        
        '''

