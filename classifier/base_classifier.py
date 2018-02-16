class BaseClassifier(object):
    '''
    BaseClassifier from which all classifier objects inherit from
    '''
    def __init__(self, classifier_name=None, data=None, labels=None, ids=None):
        self.name = classifier_name
        self.data = data
        self.labels = labels
        self.ids = ids
        self.dataset = None

    def import_data(self, data=None, labels=None, ids=None):
        '''
        Imports data into classifier

        :param data: list of data
        :param labels: list of labels
        :param ids: list of ids
        '''
        self.data = data
        self.labels = labels
        self.ids = ids

    def run_classifier(self):
        '''
        Runs the classifier
        '''
        pass