import numpy as np
from .base_classifier import BaseClassifier
from regex.handlers import CaptureHandler
from collections import defaultdict

class CaptureClassifier(BaseClassifier):
    """Class specialized in capturing information of interest. E.g Country of Birth
    """

    def __init__(self, classifier_name="CaptureClassifier", regexes=None, data=None, labels=None, ids=None, capture_biases=None, handler=CaptureHandler(), negative_label="None"):
        """
        Keyword Arguments:
            classifier_name {str} -- Name of classifier (default: {"CaptureClassifier"})
            regexes {dictionary} -- A dictionary of regex_name to a list of Regex objects (default: {None})
            data {list} -- List of data (default: {None})
            labels {list} -- List of labels (default: {None})
            ids {list} -- List of ids (default: {None})
            capture_biases {dictionary} -- A dictionary which maps the capture class name to a bias value (default: {None})
            handler {handler} --A (default: {CaptureHandler})
            negative_label {str} -- Default negative label (Used in classifications which don't fit into any class or as the negative class in single class classifciation) (default: {"None"})
        """
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)

        self.regexes = regexes
        self.capture_biases = {capture: capture_biases[capture] for capture in capture_biases} if capture_biases else {}
        self.negative_label = negative_label
        self.handler = handler 

    def classify(self, class_to_scores, threshold=0):
        """Given a dictionary of class_score, returns a tuple containing the class with the highest score and its score
        
        Arguments:
            class_to_scores {dictionary} -- class to scores
        
        Keyword Arguments:
            threshold {int} -- threshold value used to determine whether to return negative_label or classified label (default: {0})
        
        Returns:
            label {String} -- Assigned label
            score {int} -- Assigned score
        """

        #If no captures were found, return negative_label
        if len(class_to_scores) == 0:
            return self.negative_label, 0

        #Return max score
        class_name, score = max(class_to_scores.items(), key=lambda i: i[1])

        #Return negative label if less than threshold
        if score > threshold:
            return class_name, score
        else:
            return self.negative_label, 0

    def run_classifier(self, sets=["train", "valid"], class_threshold=0, preprocess_func=None, label_func=None, pwds=None):
        """Runs the trained classifier on the given datasets. Note this datasets must be loaded into self.dataset object first or
        intialized in some other manner
        
        Keyword Arguments:
            sets {list} -- Datasets to run the classifier on (default: {["train", "valid"]})
            class_threshold {int} -- threshold used to classify data as classified label or negative_label (default: {0})
            preprocess_func {function} -- sentence preprocessing function (default: {None})
            label_func {function} -- function used in labelling. Mainly used to convert 1 set of labels to another (default: {None})
            pwds {dictionary} -- Personalized word dictionaries which contain dictionary_name -> list of words (default: {None})
        """

        print("\nRunning Classifier:", self.name)

        for data_set in sets:

            assert data_set in self.dataset, "%s not in dataset" % data_set
            print("Currently classifying {} with {} datapoints".format(data_set, len(self.dataset[data_set]["data"])))

            preds = []

            data = self.dataset[data_set]["data"]

            self.dataset[data_set]["matches"] = []
            self.dataset[data_set]["scores"] = []

            for datum in data:
                capture_scores = defaultdict(int) 
                matches = {}
                captures = {}
                class_matches = {}

                #Forced to do this because self.regexes stored as {"class": [Regex Objects list]}
                for class_name in self.regexes:
                    
                    #Ask handler to get capture_scores, captures, and matches
                    if len(self.regexes[class_name]) > 0:
                        matches, captures, capture_scores = self.handler.score_and_capture_sentences(datum, self.regexes[class_name],
                                                                                                     pwds=pwds, preprocess_func=preprocess_func,
                                                                                                     capture_convert=label_func)
                    
                    #Storing matches in object
                    class_matches[class_name] = matches

                    #Adding biases
                    for bias in self.capture_biases:
                        capture_scores[bias] += self.capture_biases[bias]

                self.dataset[data_set]["matches"].append(class_matches)
                self.dataset[data_set]["scores"].append(capture_scores)

                #getting prediction
                preds.append(self.classify(capture_scores, threshold=class_threshold)[0])

            preds = np.array(preds)
            self.dataset[data_set]["preds"] = preds
