import time
import os
from datahandler import data_import as di
from classifier.simple_regex_classifier import RegexClassifier

#TODO: Remove this out of the base runner and add it elsewhere
def import_regex(regex_file, class_name=None):
    class_name = regex_file.split('.')[0] if class_name else class_name

    regexes = {}

    classifier_type, classifier_args, regexes[class_name] = di.regexes_from_csv([regex_file], [class_name], use_custom_score=True)

    classifier_type = "RegexClassifier" if not classifier_type else classifier_type

    return classifier_type, classifier_args, regexes

#TODO: Remove this out of the base runner and add it elsewhere
def import_regexes(regex_directory, class_names=None):
    file_names = os.listdir(regex_directory)
    regex_filenames = [os.path.join(regex_directory, fname) for fname in file_names]
    class_names = [(lambda file: file.split('.')[0])(file) for file in file_names] if not class_names else class_names

    regexes = {}

    classifier_type = None
    classifier_args = {}

    for class_name, file in zip(class_names, regex_filenames):
        _classifier_type, _classifier_args, regexes[class_name] = di.regexes_from_csv([file], [class_name], use_custom_score=True)
        classifier_type = _classifier_type if _classifier_type else classifier_type
        classifier_args = _classifier_args if _classifier_args else classifier_args

    classifier_type = "RegexClassifier" if not classifier_type else classifier_type

    return classifier_type, classifier_args, regexes

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
