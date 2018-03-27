from classifier.simple_regex_classifier import RegexClassifier
from classifier.simple_capture_classifier import CaptureClassifier

class Runner(object):
    def __init__(self, classifier_type, **kwargs):
        self.classifier = None

        if classifier_type == "RegexClassifier":
            self.classifier_type = RegexClassifier
        elif classifier_type == "Svm":
            pass
        elif classifier_type == "CaptureClassifier":
            self.classifier_type = CaptureClassifier

        self.classifier_parameters = {key: value for key, value in kwargs.items() if key in self.classifier_type.__init__.__code__.co_varnames[1:]}
        self.additional_params = {key: kwargs[key] for key in set(kwargs) - set(self.classifier_parameters)}

        self.classifier = self.classifier_type(**self.classifier_parameters)

    def run(self, datasets=None):
        self.classifier.run_classifier(sets=datasets, **self.additional_params)
