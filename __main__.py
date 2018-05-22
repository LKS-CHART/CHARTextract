import sys
from variable_classifiers.base_runner import Runner
from datahandler import data_import as di
import numpy as np
import functools
import os
from web.report_generator import generate_error_report
from stats.basic import calculate_accuracy
from sklearn.metrics import confusion_matrix
from stats.basic import plot_confusion_matrix, get_classification_stats, compute_ppv_accuracy_ova, \
    compute_ppv_accuracy_capture, get_classification_stats_capture
from datahandler.helpers import import_regex, import_regexes
from datahandler.preprocessors import replace_filter_by_label, replace_labels_with_required,\
    replace_label_with_required, replace_filter, convert_repeated_data_to_sublist
from classifier.classification_functions import sputum_classify, max_classify, max_month
from util.tb_country import preprocess
from util.pwd_preprocessors import PwdPreprocessor2

# Define after imports and globals
available_funcs = {}


def exposed_function(func):
    available_funcs[getattr(func,'__name__')] = func


@exposed_function
def create_regex_based_classifier(rule_path=None):
    """Creates a Regex based classifier Runner object which is later used to run the classifier

    Arguments:
        rule_path {String} -- Path to the rule directory (in the case of multiclass classification)
            or a rule file (in the case of single class classificatoin)
        ids_list {list} -- List of ids
        data_list {list} -- List of data (string) for each id

    Keyword Arguments:
        labels_list {list} -- List of labels (default: {None})
        training_mode {bool} -- Whether to run the classifier in training mode. If in training mode creates training
            and validation datasets (default: {False})
        l_id_col {int} -- Column in which label_file's ids are located starting from 0 (default: {None})
        l_label_col {int} -- Column in which label_file's labels are located starting from 0 (default: {None})
        l_first_row {int} -- From which row to start reading the data (default: {None})
        label_file {String} -- Path pointing to label file (default: {None})
        repeat_ids {bool} -- If False, ids are not considered unique and the data is appended (default: {False})
        train_percent {float} -- Percentage of training examples (default: {0.6})

    Returns:
        classifier_runner {Runner} -- Returns a Runner object which is used to run the classifier
    """

    # Import rule directory or rule file and updating classifier_args
    # Creating the Runner object with specified classifier_args
    classifier_type, classifier_args, regexes_dict = import_regexes(rule_path) \
        if os.path.isdir(rule_path) else import_regex(rule_path)
    classifier_args.update({"regexes": regexes_dict})
    runner = Runner(classifier_type, **classifier_args)

    return runner


@exposed_function
def load_classifier_data(runner, classifier_data_list, labels_list, classifier_ids_list, dataset=None,
                         create_train_valid=False, train_percent=.6, random_seed=0):
    # If training is enabled
    # Storing data within classifier and creating validation and training sets
    classifier_data_list = np.array(classifier_data_list) if classifier_data_list else None
    labels_list = np.array(labels_list) if labels_list else [None] * len(classifier_data_list)
    classifier_ids_list = np.array(classifier_ids_list) if classifier_ids_list else [None] * len(classifier_data_list)

    if not create_train_valid:
        runner.classifier.load_dataset(dataset, data=classifier_data_list, labels=labels_list, ids=classifier_ids_list)
    else:
        runner.classifier.create_train_and_valid(data=classifier_data_list, labels=labels_list, ids=classifier_ids_list,
                                                 train_percent=train_percent, random_seed=random_seed)
    return runner

'''
####
Expose certain functions that allow the following:
- Run classifier
- Change variable, datafiles/columns and labelfiles/columns
- 
####
'''
print(available_funcs)