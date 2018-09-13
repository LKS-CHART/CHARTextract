from classifier.simple_regex_classifier import RegexClassifier
from classifier.simple_capture_classifier import CaptureClassifier
from classifier.nconditional_classifier import NConditionalClassifier
from classifier.simple_regex_classifier_t import TemporalRegexClassifier

class Runner(object):
    """Generic Runner object used to initalize classifier with given args and run them
    """

    def __init__(self, classifier_type, **kwargs):
        """Initializes the Runner Object with given params
        
        Arguments:
            classifier_type {String} -- Type of classifier being initializes
        """

        self.classifier = None

        if classifier_type == "RegexClassifier":
            self.classifier_type = RegexClassifier
        elif classifier_type == "NConditionalClassifier":
            self.classifier_type = NConditionalClassifier
        elif classifier_type == "TemporalRegexClassifier":
            self.classifier_type = TemporalRegexClassifier
        elif classifier_type == "CaptureClassifier":
            self.classifier_type = CaptureClassifier

        #classifier_parameters are parameters that only appear within the __init__ function of the class
        self.classifier_parameters = {key: value for key, value in kwargs.items() if key in self.classifier_type.__init__.__code__.co_varnames[1:]}
        #Any additional parameters that were passed to the runner object but do not appear in the classifier initializer
        self.additional_params = {key: kwargs[key] for key in set(kwargs) - set(self.classifier_parameters)}

        #Initialize with params
        self.classifier = self.classifier_type(**self.classifier_parameters)

    def run(self, datasets=None, **kwargs):
        """Runs the classifier on the given datasets
        
        Keyword Arguments:
            datasets {list} - List of string corresponding to dataset names. This are datasets that will be run by the classifier (default: None)
            kwargs {function args} -- List of arguments to be passed to the run function of the classifier (default: {None})
        """

        #Parameters that are passed to the classifier at runtime
        runtime_params = {key: kwargs[key] if key in kwargs else self.additional_params[key] for key in (set(kwargs) | set(self.additional_params))}
        self.classifier.run_classifier(sets=datasets, **runtime_params)
