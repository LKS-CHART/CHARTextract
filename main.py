from classifier.regex_classifier import RegexClassifier
from classifier.ngram_classifier import NgramClassifier
from datahandler import data_import as di
import re
import os
import numpy as np

if __name__ == "__main__":

    debug = False

    if not debug:
        print("Current data folder: {!r}\n".format(os.getenv('TB_DATA_FOLDER')))
        # filenames = [os.path.normpath(os.path.join(os.getenv('DATA_FOLDER'), 'smh.ctpa.140.xlsx'))]
        data_filenames = [os.path.normpath(os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Cohort 2.csv'))]
        label_filenames = [os.path.normpath(os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx'))]
        print("Files of interest: {!r}\n".format(data_filenames))
        print("Files of interest: {!r}\n".format(label_filenames))
        #Reading excel data
        data, _, ids = di.data_from_csv(data_filenames, data_cols=2, id_cols=0, repeat_ids=False)
        _, temp_labels, temp_ids = di.data_from_excel(label_filenames, id_cols=1, label_cols=8, repeat_ids=False, first_row=2, check_col=1)
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

        #Reading regex files
        regexes = {}

        regex_dir = os.path.join('examples', 'regexes', 'tb_regexes', 'active_tb')
        regex_filenames = [os.path.join(regex_dir, fname) for fname in os.listdir(regex_dir)]

        # regexes = di.regexes_from_csv(filenames, use_customized_score=True)

        for file in regex_filenames:
            split_str = re.split(r'[\\/]+', file)
            key_name = split_str[-1].split('.')[0]
            regexes[key_name] = di.regexes_from_csv([file], [key_name], use_custom_score=True, all_matches=True)

        print(regexes)
    else:
        data, labels, ids = [],[],[]

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
    # train_ids, valid_ids = tb.create_train_and_valid(.5, 0)
    # ids = {"train": train_ids, "valid": valid_ids}

    #Running TB Classifier
    # tb.run_classifier()

    regex_list = []
    [regex_list.extend(l) for l in regexes.values()]

    #Creating Regex Classifier
    tb_regex = RegexClassifier("TB Classifier Regex", regex_list)
    tb_regex.import_data(data, labels, ids)

    train_ids_regex, valid_ids_regex = tb_regex.create_train_and_valid(0.5, 0)
    ids_regex = {"train": train_ids_regex, "valid": valid_ids_regex}

    #Running TB Classifier
    tb_regex.run_classifier()