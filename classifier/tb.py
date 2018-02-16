from .base_classifier import BaseClassifier

class TB(BaseClassifier):
    def __init__(self, data_folder):
        super().__init__(data_folder=data_folder)

    def run_classifier(self):
        print("Running Classifier")