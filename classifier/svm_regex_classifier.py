import numpy as np
from copy import copy
from .base_classifier import BaseClassifier
from util.string_functions import split_string_into_sentences
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model

class SVMRegexClassifier(BaseClassifier):
    '''
    Class specialized in classifying patient data using regexes
    '''
    def __init__(self, classifier_name, regexes, data=None, labels=None, ids=None, normalize=True):
        '''
        Initializes RegexClassifier

        :param classifier_name: Name of classifier
        :param regexes: List of Regex objects
        :param data: List of data
        :param labels: List of labels
        :param ids: List of ids
        '''
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)
        self.regexes = regexes
        self.normalize = normalize
        self.classifier = svm.SVC(kernel='linear', C=1, class_weight='balanced')

    def simple_freq_count_text(self, text, regexes, regex_to_freq_dict):
        '''
        Given a text, regexes and regex.name -> dict, it determines the amount of times regex.name appears in the text

        :param text: A string of text
        :param regexes: A list of regex objects
        :param regex_to_freq_dict: A string -> frequency dictionary i.e The regex's name to its count

        '''
        for regex in regexes:
            regex_matches = regex.determine_matches(text)
            regex_to_freq_dict[regex.name] += len(regex_matches)

    def freq_count_sentence(self, text, regexes, regex_to_freq_dict, freq_func=None):
        '''
        Given a text, regexes, regex.name and freq_func, it determines the amount of times regex.name appears in text
        using freq_func

        :param text: A string of text
        :param regexes: A list of regex objects
        :param regex_to_freq_dict: A string -> frequency dictionary i.e The regex's name to its count
        :param freq_func: function for calculating frequency
        '''
        func = self.simple_freq_count_text if freq_func is None else freq_func
        func(text, regexes, regex_to_freq_dict)

    def freq_count_sentences(self, text, regexes, regex_to_freq_dict, freq_func=None):
        '''
        Given a text, regexes, regex.name and freq_func, it determines the amount of times regex.name appears in text
        using freq_func

        :param text: A string of text
        :param regexes: A list of regex objects
        :param regex_to_freq_dict: A string -> frequency dictionary i.e The regex's name to its count
        :param freq_func: function for calculating frequency
        '''
        sentences = split_string_into_sentences(text)
        for sentence in sentences:
            self.freq_count_sentence(sentence, regexes, regex_to_freq_dict, freq_func)

    def calculate_frequency(self, dataset_name, normalize=True):
        '''
        Given a dataset_name, creates a frequency matrix where each row corresponds to the regex frequences for a single datapoint
        :param dataset_name: String dataset_name. (Note self.dataset[dataset_name] must be initialized first)
        :param normalize: If true, the frequencies are normalized to create a probability distribution else they are just counts

        :return: A nxk frequency matrix where n is the number of datapoints and k is the number of regexes
        '''
        data = self.dataset[dataset_name]["data"]
        labels = self.dataset[dataset_name]["labels"]
        ids = self.dataset[dataset_name]["ids"]

        svm_data = np.array([[]])

        for id, datum, label in zip(ids, data, labels):
            regexes_to_freq = {regex.name: 0 for regex in self.regexes}
            self.freq_count_sentences(datum, self.regexes, regexes_to_freq)

            total_val = 1

            if normalize:
                total_val = sum(regexes_to_freq.values()) if sum(regexes_to_freq.values()) > 0 else 1

            frequencies = np.array([[regexes_to_freq[regex.name]/total_val for regex in self.regexes]])

            if svm_data.shape[1] == 0:
                svm_data = frequencies
            else:
                svm_data = np.concatenate((svm_data, frequencies), axis=0)

        self.dataset[dataset_name]["regex_frequencies"] = svm_data

        return svm_data

    def train_classifier(self, **classifier_params):
        '''
        Trains SVMRegexClassifier's classifier
        '''

        data = self.calculate_frequency("train", normalize=self.normalize)
        x, y = data, self.dataset["train"]["labels"]
        self.classifier.set_params(**classifier_params)
        self.classifier.fit(x, y)

    def run_classifier(self, sets=["train", "valid"]):
        '''
        Runs the trained classifier on the given datasets. Note these must be loaded into self.dataset object first
        or initialized in some other manner

        :param sets: A list of dataset names to run the classifier on
        '''

        print("\nRunning Classifier:", self.name)

        for data_set in sets:
            print("\nRunning classifier on {} with {} datapoints\n".format(data_set, len(self.dataset[data_set]["labels"])))
            svm_data = self.calculate_frequency(data_set, normalize=self.normalize)
            preds = self.classifier.predict(svm_data)
            print("Predictions:", preds)
            print("Labels:", self.dataset[data_set]["labels"])
            wrong_indices = np.nonzero(~(preds == self.dataset[data_set]["labels"]))
            print(wrong_indices)
            # labs = np.array(['None', 'Former smoker', 'Never smoked', 'Current smoker'])
            print("Incorrect Predictions: ", preds[wrong_indices])
            print("Actual Labels: ", self.dataset[data_set]["labels"][wrong_indices])
            print("Incorrect Ids:", self.dataset[data_set]["ids"][wrong_indices])
            print(np.sum(preds == self.dataset[data_set]["labels"])/len(self.dataset[data_set]["labels"]))

        print(self.dataset["train"]["regex_frequencies"])

