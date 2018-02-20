from .base_classifier import BaseClassifier

class TB(BaseClassifier):
    '''
    Class specialized in classifying TB patient data
    '''
    def __init__(self, classifier_name="TB Classifier", data=None, labels=None, ids=None):
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)

    # def _read_data_from_folders(self, folders=None):
    #     if folders is None:
    #         folders = self.data_folders
    #
    #     for folder in folders:
    #         print(folder)


    def run_classifier(self):
        print("\nRunning Classifier:", self.name)
