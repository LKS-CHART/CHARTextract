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
    def __init__(self, classifier_name, regexes, data=None, labels=None, ids=None):
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
        self.classifier = svm.SVC(kernel='linear', C=1)

    def weighted_score_text(self, text, regexes):
        pass

    def simple_freq_count_text(self, text, regexes, regex_to_freq_dict):
        for regex in regexes:
            regex_matches = regex.determine_matches(text)
            regex_to_freq_dict[regex.name] += len(regex_matches)
            # print(regex.name, regex_to_freq_dict[regex.name])

    def freq_count_sentence(self, text, regexes, regex_to_freq_dict, freq_func=None):
        func = self.simple_freq_count_text if freq_func is None else freq_func
        func(text, regexes, regex_to_freq_dict)

    def freq_count_sentences(self, text, regexes, regex_to_freq_dict, freq_func=None):
        sentences = split_string_into_sentences(text)
        for sentence in sentences:
            self.freq_count_sentence(sentence, regexes, regex_to_freq_dict, freq_func)

    def naive_score_text(self, text, regexes):
        '''
        Naively scores text by summing the match scores in the Regex objects

        :param text: A string of text
        :param regexes: A list of Regex objects

        :return: List of Regex Objects that matched with the text, total_score
        '''

        matches = []
        total_score = 0
        for regex in regexes:

            #creating a copy because we want new unique regex objects for each match
            #reusing old regex objects will cause previous matches to be replaced by new matches and this behaviour
            #may not transfer well to multiple use cases

            regex_copy = copy(regex)
            regex_copy.clear_matches()

            #determining matches and computing score
            regex_matches = regex_copy.determine_matches(text)
            score = regex.score*len(regex_matches)

            if len(regex_matches) > 0:
                #adding the new copied regex object to matches
                matches.append(regex_copy)

            total_score += score

        return matches, total_score

    def score_sentence(self, text, regexes, score_func=None):
        '''
        Given regexes, score_func and text, determines a score for the sentence using score_func

        :param text: String of text
        :param regexes: List of Regex objects
        :param score_func: function used for scoring sentence

        :return: A list of Regex Objects that matched and total score
        '''

        func = self.naive_score_text if score_func is None else score_func
        matches, total_score = func(text, regexes)

        return matches, total_score

    def score_sentences(self, text, regexes, score_func=None):
        '''
        Given regexes, score_func and text, determines a score for the sentence using score_func

        :param text: Text to be split into sentences
        :param regexes: List of Regex Objects to search for in each sentence
        :param score_func: function used for score each sentence

        :return: {sentence_i: {'matches': [Regex Objects], 'score': sentence_score}} and a total_score
        '''

        sentences = split_string_into_sentences(text)
        matches_score_dict = {}
        total_score = 0

        for i, sentence in enumerate(sentences):
            matches, score = self.score_sentence(sentence, regexes)

            #only adding sentences that matched
            if matches:
                matches_score_dict[i] = {"matches": matches, "score": score}

            total_score += score

        return matches_score_dict, total_score

    def calculate_frequency(self, dataset_name, normalize=True):
        data = self.dataset[dataset_name]["data"]
        labels = self.dataset[dataset_name]["labels"]
        ids = self.dataset[dataset_name]["ids"]

        svm_data = np.array([[]])

        for id, datum, label in zip(ids, data, labels):
            regexes_to_freq = {regex.name: 0 for regex in self.regexes}
            self.freq_count_sentences(datum, self.regexes, regexes_to_freq)

            if normalize:
                total_val = sum(regexes_to_freq.values()) if sum(regexes_to_freq.values()) > 0 else 1

            frequencies = np.array([[regexes_to_freq[regex.name]/total_val for regex in self.regexes]])

            if svm_data.shape[1] == 0:
                svm_data = frequencies
            else:
                svm_data = np.concatenate((svm_data, frequencies), axis=0)

        self.dataset[dataset_name] = {"label_frequencies": frequencies}

        return svm_data

    def train_classifier(self):
        data = self.calculate_frequency("train")
        x, y = data, self.dataset["train"]["label"]
        self.classifier.fit(x,y)

    def load_dataset(self, data, labels, ids, dataset_name):
        pass

    def run_classifier(self, sets=["train", "valid"]):
        print("\nRunning Classifier:", self.name)

        # full_text = " ".join(self.data)
        #
        # pos_indices = self.labels == 1
        # pos_data = self.data[pos_indices]
        # neg_data = self.data[~pos_indices]
        # pos_ids = self.data[pos_indices]
        # neg_ids = self.data[~pos_indices]
        #
        # pos_text = " ".join(pos_data)
        # neg_text = " ".join(neg_data)

        # self.score_text("This is text")

        '''
        Naive classification done:
        
        id_to_match_scores = {}

        for id, datum, label in zip(self.ids, self.data, self.labels):
            matches, score = self.score_sentences(datum, self.regexes)
            id_to_match_scores[id] = {"all_matches": matches, "final_score": score}

        print(id_to_match_scores['1045'])
        '''


        '''
        
        TODO: 
        
        
        Set required labels e.g Smoking = 0, Never Smoked = 1, Past Smoker = 2
        
        create dict_1 reg_name -> freq
        
        #Used only for vanilla frequency counting. Scale frequency method will use a different technique
        For each sentence compute regex frequencies
            dict[reg_name] += freq
        
        ??Scale Frequency based on sentence index?? 
            -Potential formula
            - sum((match_index(regex_match)/len_matches)*(sentence_index/num_sentences))
                -Effect: Later terms penalized less, more matches penalized less since (1+2+3...k)/k is divergent
        
        normalize_frequencies [Perhaps unneeded if using frequency scaling, maybe not needed at all]
        
        train_svm method
            Classify data

        Consider making regex classifier more general. More parameters... Think about this more 
        '''

        svm_data, regex_to_freq = self.init_classifier()
        self.train_classifier(svm_data, self.dataset["train"]["labels"])

        for set in sets:
            preds = self.classifier.predict(self.data[set]["data"])
            wrong_indices = np.nonzero(~(preds == self.dataset[set]["labels"]))
            print(wrong_indices)
            labs = np.array(['None', 'Former smoker', 'Never smoked', 'Current smoker'])
            print("Predictions: ", labs[preds[wrong_indices]])
            print("Actual: ", labs[self.dataset[set][wrong_indices]])
            print("Ids:", self.dataset[set]["ids"][wrong_indices])
            print(preds)
            print(np.sum(preds==self.dataset[set]["labels"])/len(self.dataset[set]["labels"]))

            # print(id_to_regex_freq_data['1060'])
