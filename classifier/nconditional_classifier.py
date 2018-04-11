from .base_classifier import BaseClassifier
from regex.handlers import CaptureHandler

class NConditionalClassifier(BaseClassifier):
    """
    Class that only returns a classification if all conditions are met. Requires user-built classification function
    """

    def __init__(self, classifier_name="NConditionalClassifier", regexes=None, data=None, labels=None, ids=None, handler=TextCaptureHandler(), negative_label="None"):
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)
        self.DEBUG = False
        self.regexes = regexes
        self.negative_label = negative_label
        self.handler = handler

    def run_classifier(self, sets=["train", "valid"], preprocess_func=None, pwds=None, classify_func=None, **kwargs):
        print("\nRunning Classifier")




