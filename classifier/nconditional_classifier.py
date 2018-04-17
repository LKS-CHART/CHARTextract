from .base_classifier import BaseClassifier
from regex.handlers import TextCaptureHandler
from regex.handlers import CaptureHandler
from collections import defaultdict
import numpy as np

class NConditionalClassifier(BaseClassifier):
    """
    Class that only returns a classification if all conditions are met. Requires user-built classification function
    """

    def __init__(self, classifier_name="NConditionalClassifier", regexes=None, data=None, labels=None, ids=None, handler=CaptureHandler(), negative_label="None"):
        super().__init__(classifier_name=classifier_name, data=data, labels=labels, ids=ids)
        self.DEBUG = False
        self.regexes = regexes
        self.negative_label = negative_label
        self.handler = handler

    def run_classifier(self, sets=["train", "valid"], preprocess_func=None, pwds=None, classify_func=None, **kwargs):
        print("\nRunning Classifier", self.name)

        for data_set in sets:
            assert data_set in self.dataset, "%s not in dataset" % data_set
            print("Currently classifying {} with {} datapoints".format(data_set, len(self.dataset[data_set]["data"])))

            preds = []

            data = self.dataset[data_set]["data"]

            self.dataset[data_set]["matches"] = []
            self.dataset[data_set]["captures"] = []
            self.dataset[data_set]["scores"] = []

            for datum in data:
                class_capture_scores = {class_name: [{} for _ in range(len(datum))] for class_name in self.regexes}
                class_matches = {class_name: [{} for _ in range(len(datum))] for class_name in self.regexes} #Regex -> list of list of matches? - probably want one match in each sublist
                class_captures = {class_name: [[] for _ in range(len(datum))] for class_name in self.regexes} #Same as class_matches
                for i, case in enumerate(datum):
                    for class_name in self.regexes:
                        #Ask handler to et capture_scores, captures, and matches

                        if len(self.regexes[class_name]) > 0:
                            case_matches, case_captures, case_capture_scores = self.handler.score_data(case, self.regexes[class_name], pwds=pwds, preprocess_func=preprocess_func)

                        class_matches[class_name][i] = case_matches
                        class_captures[class_name][i] = case_captures
                        class_capture_scores[class_name][i] = case_capture_scores

                        if len(case_matches) == 0:
                            if self.DEBUG:
                                print("NConditionalClassifier: {} regex failed to match".format(class_name))
                                if class_name == "Sputum Date":
                                    print(case)
                            break

                if classify_func:
                    pred = classify_func(class_matches, class_captures, class_capture_scores)
                else:
                    pred = "None"

                self.dataset[data_set]["matches"].append(class_matches)
                self.dataset[data_set]["captures"].append(class_captures)
                self.dataset[data_set]["scores"].append(class_capture_scores)
                preds.append(pred)

        if self.DEBUG:
            print(self.dataset[data_set]["matches"])
            print(self.dataset[data_set]["captures"])

        preds = np.array(preds)
        self.dataset[data_set]["preds"] = preds
