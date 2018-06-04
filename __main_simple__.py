import json
from variable_classifiers.base_runner import Runner
from datahandler import data_import as di
import numpy as np
from web.report_generator import generate_error_report
import os
import sys
from datahandler.helpers import import_regexes2, get_rule_properties
from stats.stat_gen import get_failures
from datahandler.preprocessors import convert_repeated_data_to_sublist

orig_stdout = sys.stdout
f = open(os.devnull, 'w')
sys.stdout = f
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# Define after imports and globals
available_funcs = {}

def exposed_function(func):
    available_funcs[getattr(func,'__name__')] = func

'''
####
Expose certain functions that allow the following:
- Run classifier
- Change variable, datafiles/columns and labelfiles/columns
- 
####
'''
# simple JSON echo script


def respond(message):
    if not type(message) == dict:
        message = {'message': message}
    print(json.dumps(message), file=orig_stdout)
    orig_stdout.flush()


# MAIN RUNNING CODE
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


@exposed_function
def run_variable(variable, settings):
    template_directory = os.path.join('web', 'templates')
    effects = ["a", "aa", "ab", "r", "rb", "ra"]
    effect_colours = dict.fromkeys(["a", "aa", "ab"], "rgb(0,0,256)")
    effect_colours.update(dict.fromkeys(["r", "rb", "ra"], "rgb(256,0,0)"))

    project_settings = get_project_settings(settings)
    rules_folder = project_settings["Rules Folder"]
    pwds_folder = project_settings["Dictionaries Folder"] if "Dictionaries Folder" in project_settings else None
    pwds = di.import_pwds([os.path.join(pwds_folder, dict_name) for dict_name in os.listdir(pwds_folder)]) if pwds_folder else None

    create_train_and_valid = False if ("Create Train and Valid" not in project_settings or not
                                       project_settings["Create Train and Valid"]) else True

    prediction_mode = False if ("Prediction Mode" not in project_settings or not project_settings["Prediction Mode"]) \
        else True

    cur_run = [variable]

    DEBUG_MODE = False

    if DEBUG_MODE:
        ids, data, labels = [], [], []
        label_file = label_id_col = label_first_row = None

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

        if repeat_ids:
            ids, data, labels = convert_repeated_data_to_sublist(ids, repeated_data=data)
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
                pass

            else:
                failures_dict, error_data = get_failures(classifier_runner, cur_dataset, gen_path)
                generate_error_report(os.path.join("generated_data", rule_name, cur_dataset),
                                      template_directory, "{}".format(rule_name),
                                      classifier_runner.classifier.regexes.keys(), failures_dict, effects,
                                      custom_effect_colours=effect_colours, addition_json_params=error_data,
                                      custom_class_colours=custom_class_colours)

def run(**kwargs):
    respond({'function': 'run', 'params': kwargs})

def save(**kwargs):
    respond({'function': 'save', 'params': kwargs})

# respond({'status': 'Ready'})
for line in sys.stdin:
    x = json.loads(line)
    if x['function'] in available_funcs:
        available_funcs[x['function']](**x['params'])
        #    respond(available_funcs)
        # sys.stdout.flush()
        # globals()[x['function']](**x['params'])
        #print(json.dumps(json.loads(line)))
        respond({'status': 200})
    else:
        respond({'status': 404})
