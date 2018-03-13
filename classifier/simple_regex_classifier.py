import numpy as np
from copy import copy
from .base_classifier import BaseClassifier
from util.string_functions import split_string_into_sentences
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model
from regex.handlers import RegexHandler

class RegexClassifier(BaseClassifier):
    '''
    Class specialized in classifying patient data using regexes
    '''

    def __init__(self, classifier_name="Classifier", regexes=None, data=None, labels=None, ids=None, biases=None, multiclass=True, handler=None, negative_label="None"):
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
        self.negative_label = negative_label
        self.handler = RegexHandler() if handler is None else handler

    def classify(self, class_to_scores):
        '''
        Given a dictionary of classes_to_scores, returns a tuple containing the class with the highest_score and its score
        :param class_to_scores: Dictionary of class to scores {"class_name": score}

        :return: (class_name, score) where class_name is the class with the highest score
        '''
        return max(class_to_scores.items(), key=lambda i: i[1])

    def classify_single(self, class_to_score, threshold=0, negative_label="None"):
        label, score = list(class_to_score.items())[0]

        if score > threshold:
            return label
        else:
            return negative_label

    def run_classifier(self, sets=["train", "valid"], single_class_threshold=0):
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

            data = self.dataset[data_set]["data"]

            self.dataset[data_set]["matches"] = []
            self.dataset[data_set]["scores"] = []

            for datum in data:
                class_scores = {}
                class_matches = {}
                for class_name in self.regexes:
                    matches = []
                    score = 0
                    if len(self.regexes[class_name]) > 0:
                        matches, score = self.handler.score_and_match_sentences(datum, self.regexes[class_name])

                    class_scores[class_name] = self.biases[class_name] + score
                    class_matches[class_name] = matches

                self.dataset[data_set]["matches"].append(class_matches)
                self.dataset[data_set]["scores"].append(class_scores)

                if self.multiclass:
                    preds.append(self.classify(class_scores)[0])
                else:
                    preds.append(self.classify_single(class_scores, single_class_threshold, self.negative_label))

            preds = np.array(preds)
            self.dataset[data_set]["preds"] = preds
