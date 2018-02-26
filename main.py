from classifier.svm_regex_classifier import SVMRegexClassifier
from classifier.simple_regex_classifier import RegexClassifier
from classifier.ngram_classifier import NgramClassifier
from datahandler import data_import as di
import re
import os
import numpy as np
from util.string_functions import split_string_into_sentences

if __name__ == "__main__":

    debug = False

    #Reading regex files
    regexes = {}

    regex_dir = os.path.join('examples', 'regexes', 'tb_regexes', 'smoking')
    regex_filenames = [os.path.join(regex_dir, fname) for fname in os.listdir(regex_dir)]

    # regexes = di.regexes_from_csv(filenames, use_customized_score=True)

    for file in regex_filenames:
        split_str = re.split(r'[\\/]+', file)
        key_name = split_str[-1].split('.')[0]
        regexes[key_name] = di.regexes_from_csv([file], [key_name], use_custom_score=True, all_matches=False)

    regexes["None"] = []

    print(regexes)

    if not debug:
        print("Current data folder: {!r}\n".format(os.getenv('TB_DATA_FOLDER')))
        # filenames = [os.path.normpath(os.path.join(os.getenv('DATA_FOLDER'), 'smh.ctpa.140.xlsx'))]
        data_filenames = [os.path.normpath(os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Cohort 2 (cleansed).csv'))]
        label_filenames = [os.path.normpath(os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx'))]
        print("Files of interest: {!r}\n".format(data_filenames))
        print("Files of interest: {!r}\n".format(label_filenames))

        #Reading excel data
        data, _, ids = di.data_from_csv(data_filenames, data_cols=2, id_cols=0, repeat_ids=False)
        _, temp_labels, temp_ids = di.data_from_excel(label_filenames, id_cols=1, label_cols=7, repeat_ids=False, first_row=2, check_col=1)
        # print(temp_labels)
        # print(len(temp_labels))
        # print(np.sum([1 if label == 'Active TB' or  label == 'None' else 0 for label in temp_labels]))
        labels = ["None"] * len(data)
        count = 0
        for i, data_id in enumerate(ids):
            if data_id in temp_ids:
                labels[i] = temp_labels[temp_ids.index(data_id)]
            else:
                count += 1

        print("\n\nTraining data tuples:\n")
        print(list(zip(data, labels, ids)))

    else:
        data = ['I am a smoker.', 'She does not smoke.', 'She used to smoke', 'Current smoker.', 'I am a patient.']
        labels = ['Current smoker', 'Never smoked', 'Former smoker', 'Current smoker', 'None']
        ids = ['0', '1', '2', '3', '4']

    #Creating TB Classifier
    # tb = NgramClassifier("TB Classifier 1")
    #
    # tb.import_data(data, labels, ids)
    #
    # #Setting all positive examples to 1
    # tb.labels[tb.labels == 'y'] = 1
    # tb.labels[tb.labels == 'n'] = 0
    #
    # #Removing that one example which has value 10 in the labels
    # tb.labels = tb.labels[:-1]
    # tb.data = tb.data[:-1]
    # tb.ids = tb.ids[:-1]
    #
    # tb.labels = tb.labels.astype(np.float)
    #
    # train_ids, valid_ids = tb.create_train_and_valid(.5, 0)dd
    # ids = {"train": train_ids, "valid": valid_ids}

    #Running TB Classifier
    # tb.run_classifier()

    regex_list = []
    [regex_list.extend(l) for l in regexes.values()]

    #Creating Regex Classifier
    tb_regex = SVMRegexClassifier("Smoking Classifier", regex_list, normalize=True)
    tb_regex.import_data(data, labels, ids)

    #Converting label names to values
    tb_regex.labels[tb_regex.labels == 'None'] = 0
    tb_regex.labels[tb_regex.labels == 'Former smoker'] = 1
    tb_regex.labels[tb_regex.labels == 'Never smoked'] = 2
    tb_regex.labels[tb_regex.labels == 'Current smoker'] = 3

    tb_regex.labels = tb_regex.labels.astype(np.int32)

    train_ids_regex, valid_ids_regex = tb_regex.create_train_and_valid(0.75, 0)
    ids_regex = {"train": train_ids_regex, "valid": valid_ids_regex}

    #Running Smoking Classifier
    # tb_regex.load_dataset("train", tb_regex.data, tb_regex.labels, tb_regex.ids)
    tb_regex.train_classifier()
    tb_regex.run_classifier(sets=["train", "valid"])

    #Creating Naive Regex Classifier
    regex_biases = {regex_name: 0 for regex_name in regexes}
    regex_biases["None"] = 1
    tb_regex_naive = RegexClassifier("Basic Smoking Classifier", regexes, multiclass=True, biases=regex_biases)
    tb_regex_naive.import_data(data, labels, ids)

    #Converting label names to values
    tb_regex_naive.labels[tb_regex_naive.labels == 'None'] = 'None'
    tb_regex_naive.labels[tb_regex_naive.labels == 'Former smoker'] = 'former_smoker'
    tb_regex_naive.labels[tb_regex_naive.labels == 'Never smoked'] = 'never_smoker'
    tb_regex_naive.labels[tb_regex_naive.labels == 'Current smoker'] = 'current_smoker'

    tb_regex_naive.create_train_and_valid(0.7, 0)

    #Running Naive Smoking Classifier
    tb_regex_naive.run_classifier(sets=["train", "valid"])
