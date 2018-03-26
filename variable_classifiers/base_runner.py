import time
import os
from datahandler import data_import as di
from classifier.simple_regex_classifier import RegexClassifier

class Runner(object):
    def __init__(self, classifier_type, **kwargs):
        self.preds = []
        self.scores = []
        self.matches = []
        self.classifier = None
        #Make this more generic in the future.. i.e don't assume that the classifier will be using regexes
        #pass in functor list. Evaluate functors at given args

        if classifier_type == "RegexClassifier":
            self.classifier_type = RegexClassifier
        elif classifier_type == "Svm":
            pass
        else:
            self.classifier_type = None

        self.classifier_parameters = {key: value for key, value in kwargs.items() if key in self.classifier_type.__init__.__code__.co_varnames[1:]}
        self.additional_params = {key: kwargs[key] for key in set(kwargs) - set(self.classifier_parameters)}

        self.classifier = self.classifier_type(**self.classifier_parameters)

    def run(self, ids, data, labels=None, train=False, train_percent=0.6):
        if not train:
            self.classifier.load_dataset("test", data=data, ids=ids)
            self.classifier.run_classifier(sets=["test"], **self.additional_params)
        else:
            self.classifier.import_data(data=data, ids=ids, labels=labels)
            self.classifier.create_train_and_valid(train_percent)
            self.classifier.run_classifier(sets=["train", "valid"], **self.additional_params)

