import numpy as np
from .base_classifier import BaseClassifier
from regex.handlers import RegexHandler

class RegexClassifier(BaseClassifier):
    """Class specialized in classifying data using regexes
    """

    def __init__(self, classifier_name="RegexClassifier", regexes=None, data=None, labels=None, ids=None, biases=None, handler=RegexHandler(), negative_label="None"):
        """Initializes RegexClassifier
        
        Keyword Arguments:
            classifier_name {str} -- Name of classifier (default: {"RegexClassifier"})
            regexes {[type]} -- A dictionary of regex_name to a list of Regex objects (default: {None})
            data {list} -- List of data (default: {None})
            labels {list} -- List of labels (default: {None})
            ids {list} -- List of ids (default: {None})
            biases {dictionary} -- Dictionary which maps a class name to a bias (default: {None})
            handler {Handler} -- Handler used for scoring sentences (default: {RegexHandler})
            negative_label {str} -- Default negative label (Used in classifications which don't fit into any class or as the negative class in single class classifciation) (default: {"None"})

        """
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)

        self.regexes = regexes
        self.biases = {class_name: 0 for class_name in self.regexes}
        self.negative_label = negative_label
        self.handler = handler


        #TODO: Think about this... I don't think we need a separate regex key or bias for None. Negative label bias idea is encapsulated by threshold anyway
        # if biases:
        #     self.biases.update({negative_label: 0})
        #     self.regexes.update({negative_label: []})

        if biases:
            self.set_biases(biases)

    def set_biases(self, bias_dict={}):
        self.biases.update(bias_dict)

    def classify(self, class_to_scores, threshold=0):
        """Given a dictionary of classes_to_scores, returns a tuple containing the class with the highest_score and its score
        
        Arguments:
            class_to_scores {dictionary} -- dictionary which class_name to a score
        
        Keyword Arguments:
            threshold {int} -- threshold value used to determine whether to return negative_label or classified label (default: {0})
            negative_label {str} -- [description] (default: {"None"})
        
        Returns:
            label {String} -- Assigned label
            score {int} -- Assigned score
        """
        label, score = max(class_to_scores.items(), key=lambda i: i[1])
        print(class_to_scores.items())
        #Return negative label if less than threshold
        if score > threshold:
            return label, score
        else:
            return self.negative_label, score

    #TODO: Add preprocessing function
    def run_classifier(self, sets=["train", "valid"], class_threshold=0, pwds=None, label_func=None):

        """Runs the trained classifier on the given datasets. Note this datasets must be loaded into self.dataset object first or
        intialized in some other manner
        
        Keyword Arguments:
            sets {list} -- Datasets to run the classifier on (default: {["train", "valid"]})
            class_threshold {int} -- threshold used to classify data as classified label or negative_label (default: {0})
        """

        print("\nRunning Classifier:", self.name)

        for data_set in sets:
            print("Currently classifying {} with {} datapoints".format(data_set, len(self.dataset[data_set]["data"])))

            preds = []

            data = self.dataset[data_set]["data"]
            ids = self.dataset[data_set]["ids"]

            self.dataset[data_set]["matches"] = []
            self.dataset[data_set]["scores"] = []

            for id,datum in zip(ids,data):
                print("Classifying id: ", id)
                class_scores = {}
                class_matches = {}
                for class_name in self.regexes:
                    matches = []
                    score = 0

                    #matching sentences and computing scores
                    if len(self.regexes[class_name]) > 0:
                        matches, score = self.handler.score_and_match_sentences(datum, self.regexes[class_name], pwds=pwds)
                        # print(score)

                    #adding biases
                    class_scores[class_name] = self.biases[class_name] + score
                    #storing matches for that class
                    class_matches[class_name] = matches

                self.dataset[data_set]["matches"].append(class_matches)
                self.dataset[data_set]["scores"].append(class_scores)

                classification, score = self.classify(class_scores, class_threshold)
                preds.append(classification)

                print("Score: ", score)
                print("Classification: ", classification)
                print("END DATUM\n\n")
            preds = np.array(preds)
            print(preds)
            self.dataset[data_set]["preds"] = preds
