import numpy as np

class BaseClassifier(object):
    """
    BaseClassifier from which all classifier objects inherit from
    """
    def __init__(self, classifier_name="Classifier", data=None, labels=None, ids=None):
        """Initializaes BaseClassifier

        Keyword Arguments:
            classifier_name {String} -- Name of the classifier (default: {None})
            data {list} -- List of data (default: {None})
            labels {list} -- List of labels (default: {None})
            ids {list} -- List of ids (default: {None})
        """

        self.name = classifier_name
        self.data = data
        self.labels = labels
        self.ids = ids
        self.dataset = {"train": {"ids": [], "labels": [], "data": [], "preds": [], "matches": []},
                           "valid": {"ids": [], "labels": [], "data": [], "preds": [], "matches": []},
                           "test": {"ids": [], "labels": [], "data": [], "preds": [], "matches": []}}

    def load_dataset(self, dataset_name, data=None, labels=None, ids=None):
        """Load a dataset into classifier object
        
        Arguments:
            dataset_name {String} -- Name of the dataset that is being loaded. Used as a key to a dictionary
        
        Keyword Arguments:
            data {numpy array} -- np array of data (default: {None})
            labels {numpy array} -- np array of labels (default: {None})
            ids {numpy array} -- np array of ids (default: {None})
        """

        self.dataset[dataset_name] = {"ids": ids, "labels": labels, "data": data,
                                                     "preds": [], "matches": []}

    def import_data(self, data=None, labels=None, ids=None):
        """Import data into the classifier
        
        Keyword Arguments:
            data {list} -- list of data (default: {None})
            labels {list} -- list of labels (default: {None})
            ids {list} -- list of ids (default: {None})
        """
        self.data = np.array(data) if data else None
        self.labels = np.array(labels) if labels else None
        self.ids = np.array(ids) if ids else None

    def create_train_and_valid(self, train_percent=.6, random_seed=None):
        """Splits data in train and valid
        
        Keyword Arguments:
            train_percent {float} -- Ratio of train/total (default: {.6})
            random_seed {int} -- Seed for RandomState (default: {None})
        
        Returns:
            train ids{list} -- List of train ids
            valid ids{list} -- List of valid ids
        """
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
        """Runs the classifier
        """

        pass