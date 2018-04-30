from .base_classifier import BaseClassifier
from regex.handlers import RegexHandler
from util.string_functions import split_string_into_sentences
import numpy as np

class TemporalRegexClassifier(BaseClassifier):

    def __init__(self, classifier_name="TemporalRegexClassifier", regexes=None, data=None, labels=None, ids=None,
                 biases=None, handler=RegexHandler(), negative_label="None"):

        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)
        self.DEBUG = False
        self.regexes = regexes
        self.biases = {class_name: 0 for class_name in self.regexes}
        self.negative_label = negative_label
        self.handler = handler

        #TODO: Think about this... I don't think we need a separate regex key or bias for None. Negative label bias idea is encapsulated by threshold anyway

        self.biases.update({negative_label: 0})
        self.regexes.update({negative_label: []})

        if biases:
            self.set_biases(biases)

    def set_biases(self, bias_dict={}):
        self.biases.update(bias_dict)

    def classify(self, class_to_scores, threshold=0):
        """Given a dictionary of classes_to_scores, returns a tuple containing the class with the highest_score and its score

        Arguments:
            class_to_scores {dictionary} -- dictionary which class_name to a score

        Keyword Arguments:
            threshold {int} -- threshold value used to determine whether to return negative_label or classified label (default: {0})
            negative_label {str} -- [description] (default: {"None"})

        Returns:
            label {String} -- Assigned label
            score {int} -- Assigned score
        """
        label, score = max(class_to_scores.items(), key=lambda i: i[1])
        if self.DEBUG:
            print(class_to_scores.items())
        #Return negative label if less than threshold
        if score > threshold:
            return label, score
        else:
            return self.negative_label, score

    def _get_case_lengths(self, datum):

        sentence_start_list = [0]*len(datum)

        for i in range(1, len(datum)):
            sentence_start_list[i] = sentence_start_list[i-1] + len(split_string_into_sentences(datum[i-1]))

        return sentence_start_list

    def run_classifier(self, sets=["train", "valid"], class_threshold=0, pwds=None, label_func=None,
                       classify_func=None, **kwargs):

        print("\nRunning Classifier", self.name)

        for data_set in sets:
            assert data_set in self.dataset, "%s not in dataset" % data_set
            print("Currently classifying {} with {} datapoints".format(data_set, len(self.dataset[data_set]["data"])))

            preds = []

            data = self.dataset[data_set]["data"]
            self.dataset[data_set]["matches"] = []
            self.dataset[data_set]["scores"] = []

            for data_index, datum in enumerate(data):
                print("-"*100)
                print("Classifying id: ", self.dataset[data_set]["ids"][data_index])
                print("Label: ", self.dataset[data_set]["labels"][data_index])
                #Regex -> list of list of matches? - probably want one match in each sublist

                class_matches = [{class_name: {} for class_name in self.regexes} for _ in range(len(datum))]
                class_scores = [{class_name: 0 for class_name in self.regexes} for _ in range(len(datum))]

                unrolled_class_matches = {class_name: {} for class_name in self.regexes}

                latest_index_w_matches = 0

                case_lengths = self._get_case_lengths(datum)
                print(case_lengths)

                for i, case in enumerate(datum):
                    index_start = case_lengths[i]

                    for class_name in self.regexes:
                        if len(self.regexes[class_name]) > 0:

                            case_matches, case_score = self.handler.score_data(case, self.regexes[class_name],
                                                                               pwds=pwds, index_start=index_start)

                        class_scores[i][class_name] = self.biases[class_name] + case_score

                        #storing matches for that class
                        class_matches[i][class_name] = case_matches

                        if (case_score > 0 or case_score < 0):
                            latest_index_w_matches = i

                        unrolled_class_matches[class_name].update(case_matches)

                if not classify_func:
                    classification, score = self.classify(class_scores[latest_index_w_matches],
                                                                        class_threshold)
                else:
                    classification = classify_func(class_matches[latest_index_w_matches], None,
                                                   class_scores[latest_index_w_matches],
                                                   negative_label=self.negative_label, **kwargs)

                self.dataset[data_set]["matches"].append(unrolled_class_matches)
                self.dataset[data_set]["scores"].append(class_scores)

                preds.append(classification)

        if self.DEBUG:
            print(self.dataset[data_set]["matches"])

        preds = np.array(preds)
        self.dataset[data_set]["preds"] = preds
