class BaseClassifier(object):
    def __init__(self, classifier_name=None, data=None, labels=None, ids=None):
        self.name = classifier_name
        self.data = data
        self.labels = labels
        self.ids = ids
        self.dataset = None

    def run_classifier(self):
        pass