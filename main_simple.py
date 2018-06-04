from variable_classifiers.base_runner import Runner
import numpy as np
from web.report_generator import generate_error_report
from datahandler.helpers import import_regexes2, get_rule_properties
import os
import json
from datahandler import data_import as di
import argparse
import csv
from stats.stat_gen import get_failures

"""
Project has project settings json. Specifies a single data file.
Can specify a label file. If create train and valid is true, creates a train
and validation set.


Each Rule folder contains a rule properties json which specifies label column(s)
and a label_func

Each Rule folder has a classifier properties json which specifies classifier properties
minus the positive label which will be specified within the regex file.
"""

def create_regex_based_classifier(rule_path=None):
    classifier_type, classifier_args, regexes_dict = import_regexes2(rule_path) if os.path.isdir(rule_path) else None
    classifier_args.update({"regexes": regexes_dict})
    runner = Runner(classifier_type, **classifier_args)

    return runner

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
        runner.classifier.create_train_and_valid(ids=classifier_ids_list, data=classifier_data_list, labels=labels_list,
                                                 train_percent=train_percent, random_seed=random_seed)
    return runner

def get_project_settings(project_settings_path=None):
    '''
    Data json contains:

    Data File:
    Label File:
    Rules Folder:
    Create Train and Valid:
    Prediction Mode:
    Dictionaries Folder:

    :param project_settings_path:
    :return:
    '''
    with open(project_settings_path) as json_f:
        data = json.load(json_f)

    return data


if __name__ == "__main__":
    template_directory = os.path.join('web', 'templates')
    effects = ["a", "aa", "ab", "r", "rb", "ra"]
    effect_colours = dict.fromkeys(["a", "aa", "ab"], "rgb(0,0,256)")
    effect_colours.update(dict.fromkeys(["r", "rb", "ra"], "rgb(256,0,0)"))

    parser = argparse.ArgumentParser()

    parser.add_argument("settings", metavar="S", type=str, help="Project Settings File")
    parser.add_argument('-f', action='store', dest='cur_run_f',
                        help='File that contains a list of variables to run')

    parser.add_argument('-l', '--list', nargs='+', dest="cur_run",
                        help='Variables to run')

    parser.add_argument('-D', '--debug', dest="debug", action="store_true", default=False,
                        help="Runs Program in Debug Mode")

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    project_settings = get_project_settings(args.settings)
    rules_folder = project_settings["Rules Folder"]
    pwds_folder = project_settings["Dictionaries Folder"] if "Dictionaries Folder" in project_settings else None
    pwds = di.import_pwds([os.path.join(pwds_folder, dict_name) for dict_name in os.listdir(pwds_folder)]) if pwds_folder else None

    create_train_and_valid = False if ("Create Train and Valid" not in project_settings or not
                                       project_settings["Create Train and Valid"]) else True

    prediction_mode = False if ("Prediction Mode" not in project_settings or not project_settings["Prediction Mode"]) \
        else True

    cur_run = list(filter(lambda f: os.path.isdir(f), os.listdir(rules_folder)))

    if args.cur_run_f:
        with open(args.cur_run_f) as c_file:
            rows = csv.reader(c_file, delimiter=',', quotechar='"')
            cur_run = [var.strip() for row in rows for var in row]

    if args.cur_run:
        cur_run = args.cur_run

    DEBUG_MODE = args.debug

    if DEBUG_MODE:
        ids, data, labels = [], [], []
        label_file = label_id_col = label_first_row = label_func = None

    else:
        data_file = project_settings["Data File"]
        data_id_cols = project_settings["Data Id Cols"]
        data_first_row = project_settings["Data First Row"]
        data_cols = project_settings["Data Cols"]
        repeat_ids = not project_settings["Concatenate Data"]

        if not prediction_mode:
            label_file = project_settings["Label File"]
            label_id_col = project_settings["Label Id Col"]
            label_first_row = project_settings["Label First Row"]
        else:
            label_file = label_id_col = label_first_row = None

        data_loader = di.data_from_csv if data_file.endswith('.csv') else di.data_from_excel
        data, _, ids = data_loader([data_file], data_cols=data_cols, first_row=data_first_row,
                                   id_cols=data_id_cols, repeat_ids=repeat_ids)

    for rule in cur_run:
        rule_file = os.path.join(rules_folder, rule)
        rule_name = rule

        print("="*100)
        classifier_runner = create_regex_based_classifier(rule_file)

        label_col, label_func, classifier_runtime_args = get_rule_properties(rule_file, rule_name, pwds)
        available_datasets = ["train"]

        if not prediction_mode:

            labels = None

            if not DEBUG_MODE:
                ids, data, labels = di.get_labeled_data(ids, data, label_file, label_id_col, label_col, label_first_row,
                                                        label_func)

            if create_train_and_valid:
                classifier_runner = load_classifier_data(classifier_runner, data, labels, ids,
                                                         create_train_valid=True, train_percent=.6, random_seed=0)
                available_datasets = ["train", "valid"]

            else:
                classifier_runner = load_classifier_data(classifier_runner, data, labels,
                                                         ids, dataset=available_datasets[0])

        else:
            labels = [None]*len(data)
            classifier_runner = load_classifier_data(classifier_runner, data, labels,
                                                     ids, dataset=available_datasets[0])

        #available_datasets = ["train"]
        for cur_dataset in available_datasets:
            print("\nRunning on rule: {} - {}".format(rule_name, cur_dataset))
            gen_path = os.path.join("generated_data", rule_name, cur_dataset)

            classifier_classes = sorted(list(classifier_runner.classifier_parameters["regexes"]))
            custom_class_colours = None

            if len(classifier_classes) == 2:
                negative_label = classifier_runner.classifier.negative_label
                positive_label = next(filter(lambda i: i != negative_label, classifier_classes))
                custom_class_colours = {negative_label: "hsl({},{}%,{}%)".format(15,71.4,89),
                                        positive_label: "hsl({},{}%,{}%)".format(97,81,91.8)}

            if not os.path.exists(gen_path):
                os.makedirs(gen_path)

            if classifier_runtime_args:
                classifier_runner.run(datasets=[cur_dataset], **classifier_runtime_args)
            else:
                classifier_runner.run(datasets=[cur_dataset])

            if prediction_mode:
                print("Running in Prediction Mode")
                pass

            else:
                failures_dict, error_data = get_failures(classifier_runner, cur_dataset, gen_path)
                generate_error_report(os.path.join("generated_data", rule_name, cur_dataset),
                                      template_directory, "{}".format(rule_name),
                                      classifier_runner.classifier.regexes.keys(), failures_dict, effects,
                                      custom_effect_colours=effect_colours, addition_json_params=error_data,
                                      custom_class_colours=custom_class_colours)
