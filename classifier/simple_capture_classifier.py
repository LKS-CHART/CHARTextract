import numpy as np
from .base_classifier import BaseClassifier
from regex.handlers import CaptureHandler

class CaptureClassifier(BaseClassifier):
    '''
    Class specialized in capturing information of interest. E.g Country of birth
    '''

    def __init__(self, classifier_name="CaptureClassifier", regexes=None, data=None, labels=None, ids=None, capture_biases=None, handler=None, negative_label="None", pwds=None):
        '''
        Initializes Capture Classifier

        :param classifier_name: Name of classifier
        :param regexes: A dictionary of regex_name to a list of Regex objects
        :param data: List of data
        :param labels: List of labels
        :param ids: List of ids
        '''
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)

        self.regexes = regexes
        self.capture_biases = {capture: capture_biases[capture] for capture in capture_biases}
        self.negative_label = negative_label
        self.handler = CaptureHandler() if handler is None else handler
        self.pwds = pwds

    def classify(self, class_to_scores, threshold=0):
        '''
        Given a dictionary of classes_to_scores, returns a tuple containing the class with the highest_score and its score
        :param class_to_scores: Dictionary of class to scores {"class_name": score}

        :return: (class_name, score) where class_name is the class with the highest score
        '''
        class_name, score = max(class_to_scores.items(), key=lambda i: i[1])

        if score > threshold:
            return class_name, score
        else:
            return self.negative_label, 0

    def run_classifier(self, sets=["train", "valid"], class_threshold=0, preprocess_func=None, label_func=None):
        '''
        Runs the trained classifier on the given datasets. Note these datasets must be loaded into self.dataset object first
        or initialized in some other manner

        :param sets: A list of dataset names to run the classifier on
        '''

        print("\nRunning Classifier:", self.name)

        for data_set in sets:
            print("Currently classifying {} with {} datapoints".format(data_set, len(self.dataset[data_set]["data"])))

            preds = []

            data = self.dataset[data_set]["data"]

            self.dataset[data_set]["matches"] = []
            self.dataset[data_set]["scores"] = []

            for datum in data:
                capture_scores = {}
                matches = {}
                captures = {}
                class_matches = {}

                #Assumes only 1 capturing class (e.g country of birth)
                for class_name in self.regexes:
                    #Class captures and scores
                    #E.g
                    #??captures["canada"] = 23231??
                    #captures = {sentence_i: {matches}}

                    if len(self.regexes[class_name]) > 0:
                        matches, captures, capture_scores = self.handler.score_and_capture_sentences(datum, self.regexes[class_name],
                                                                                                     pwds=self.pwds, preprocess_func=preprocess_func,
                                                                                                     capture_convert=label_func)
                    class_matches[class_name] = matches

                    for bias in self.capture_biases:
                        capture_scores[bias] += self.capture_biases[bias]

                self.dataset[data_set]["matches"].append(class_matches)
                self.dataset[data_set]["scores"].append(capture_scores)

                preds.append(self.classify(capture_scores)[0])

            preds = np.array(preds)
            self.dataset[data_set]["preds"] = preds
