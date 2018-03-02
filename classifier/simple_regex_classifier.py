import numpy as np
from copy import copy
from .base_classifier import BaseClassifier
from util.string_functions import split_string_into_sentences
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model

class RegexClassifier(BaseClassifier):
    '''
    Class specialized in classifying patient data using regexes
    '''
    def __init__(self, classifier_name, regexes, data=None, labels=None, ids=None, biases=None, multiclass=True):
        '''
        Initializes RegexClassifier

        :param classifier_name: Name of classifier
        :param regexes: A dictionary of regex_name to a list of Regex objects
        :param data: List of data
        :param labels: List of labels
        :param ids: List of ids
        '''
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)
        self.regexes = regexes
        self.biases = biases
        self.multiclass = multiclass

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
                matches_score_dict[i] = {"matches": matches, "text_score": score}

            total_score += score

        return matches_score_dict, total_score

    def classify(self, class_to_scores):
        '''
        Given a dictionary of classes_to_scores, returns a tuple containing the class with the highest_score and its score
        :param class_to_scores: Dictionary of class to scores {"class_name": score}

        :return: (class_name, score) where class_name is the class with the highest score
        '''
        return max(class_to_scores.items(), key=lambda i: i[1])

    def run_classifier(self, sets=["train", "valid"]):
        '''
        Runs the trained classifier on the given datasets. Note these datasets must be loaded into self.dataset object first
        or initialized in some other manner

        :param sets: A list of dataset names to run the classifier on
        '''

        print("\nRunning Classifier:", self.name)

        '''
        ??Scale Frequency based on sentence index?? 
            -Potential formula
            - sum((match_index(regex_match)/len_matches)*(sentence_index/num_sentences))
                -Effect: Later terms penalized less, more matches penalized less since (1+2+3...k)/k is divergent
        
        '''

        for data_set in sets:
            print("Currently classifying {} with {} datapoints".format(data_set, len(self.dataset[data_set]["data"])))

            preds = []

            ids = self.dataset[data_set]["ids"]
            data = self.dataset[data_set]["data"]
            labels = self.dataset[data_set]["labels"]
            self.dataset[data_set]["matches"] = []
            self.dataset[data_set]["scores"] = []

            for id, datum, label in zip(ids, data, labels):
                class_scores = {}
                class_matches = {}
                for class_name in self.regexes:
                    matches = []
                    score = 0
                    if len(self.regexes[class_name]) > 0:
                        matches, score = self.score_sentences(datum, self.regexes[class_name])

                    class_scores[class_name] = self.biases[class_name] + score
                    class_matches[class_name] = matches

                self.dataset[data_set]["matches"].append(class_matches)
                self.dataset[data_set]["scores"].append(class_scores)
                preds.append(self.classify(class_scores)[0])

            preds = np.array(preds)
            self.dataset[data_set]["preds"] = preds
