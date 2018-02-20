import numpy as np

class BaseClassifier(object):
    '''
    BaseClassifier from which all classifier objects inherit from
    '''
    def __init__(self, classifier_name=None, data=None, labels=None, ids=None):
        self.name = classifier_name
        self.data = data
        self.labels = labels
        self.ids = ids
        self.dataset = {"train": {"ids": [], "labels": [], "data": [], "preds": [], "scores": [], "matches": []},
                           "valid": {"ids": [], "labels": [], "data": [], "preds": [], "scores": [], "matches": []},
                           "test": {"ids": [], "labels": [], "data": [], "preds": [], "scores": [], "matches": []}}

    def import_data(self, data=None, labels=None, ids=None):
        '''
        Imports data into classifier

        :param data: list of data
        :param labels: list of labels
        :param ids: list of ids
        '''

        self.data = np.array(data)
        self.labels = np.array(labels)
        self.ids = np.array(ids)

    def create_train_and_valid(self, train_percent=.6, random_seed=None):
        '''
        Splits data in train and valid

        :param train_percent: Ratio of train/total
        :param random_seed: Seed for RandomState
        :return: List train ids, list of valid ids

        '''

        if random_seed is not None:
            randomizer = np.random.RandomState(random_seed)
        else:
            randomizer = np.random.RandomState()

        x = randomizer.permutation(len(self.data))
        train = np.sort(x[:int(len(x) * train_percent)])
        valid = np.sort(x[int(len(x) * train_percent):])

        self.dataset["train"]["data"] = self.data[train]
        self.dataset["train"]["labels"] = self.labels[train]
        self.dataset["train"]["ids"] = self.ids[train]

        self.dataset["valid"]["data"] = self.data[valid]
        self.dataset["valid"]["labels"] = self.labels[valid]
        self.dataset["valid"]["ids"] = self.ids[valid]

        for each in ["train", "valid"]:
            self.dataset[each]["preds"] = [None] * len(self.dataset[each]["data"])
            self.dataset[each]["scores"] = [None] * len(self.dataset[each]["data"])
            self.dataset[each]["matches"] = [None] * len(self.dataset[each]["data"])

        return self.ids[train], self.ids[valid]

    def run_classifier(self):
        '''
        Runs the classifier
        '''

        pass