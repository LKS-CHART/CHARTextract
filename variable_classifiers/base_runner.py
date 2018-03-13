import os
from datahandler import data_import as di
from classifier.simple_regex_classifier import RegexClassifier

#Probably want to remove this out of the base runner and add it to some child class
def import_regexes(regex_directory, class_names=None, multiclass=True):
    file_names = os.listdir(regex_directory)
    regex_filenames = [os.path.join(regex_directory, fname) for fname in file_names]
    class_names = [(lambda file: file.split('.')[0])(file) for file in file_names] if not class_names else class_names

    regexes = {}

    for class_name, file in zip(class_names, regex_filenames):
        regexes[class_name] = di.regexes_from_csv([file], [class_name], use_custom_score=True)

    if multiclass:
        regexes["None"] = []

    return regexes

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
        self._multiclass = self.classifier_parameters['multiclass'] if 'multiclass' in self.classifier_parameters else True
        self.additional_params = {key: kwargs[key] for key in set(kwargs) - set(self.classifier_parameters)}

        self.classifier = self.classifier_type(**self.classifier_parameters)

    def run(self, ids, data):
        self.classifier.load_dataset("test", data=data, ids=ids)
        self.classifier.run_classifier(sets=["test"], **self.additional_params)
