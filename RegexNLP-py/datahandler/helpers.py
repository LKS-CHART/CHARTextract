import os
from datahandler import data_import as di
import json
from util.pwd_preprocessors import PwdPreprocessor2
from properties2 import *
import importlib.util

def settings_factory(settings_path):
    """
    PREPROCESS_DATA_FUNC = f_data
    PREPROCESS_LABEL_FUNC = f_label
    PREPROCESS_SENTENCE = f
    HANDLER = handler()
    CLASSIFY_FUNC = f_classification
    """
    settings_mappings = {
      "Runner Initialization Params": {
        "HANDLER": "handler",
        "PREPROCESS_LABEL_FUNC": "label_func",
        "PREPROCESS_DATA_FUNC": "data_func"
      },
      "Runtime Params": {
          "CLASSIFY_FUNC": "classify_func",
          "PREPROCESS_SENTENCE": "preprocess_func"
    }}

    spec = importlib.util.spec_from_file_location("python.settings", settings_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    settings_dictionary = {}
    settings_globals = module.__dict__

    for param_type in settings_mappings:
        if param_type not in settings_dictionary:
            settings_dictionary[param_type] = {}

        for setting in settings_mappings[param_type]:
            mapped_setting = settings_mappings[param_type][setting]

            if setting in settings_globals:
                settings_dictionary[param_type][mapped_setting] = settings_globals[setting]

    return settings_dictionary

def import_regex(regex_file):
    """Import a single regex rule file

    Arguments:
        regex_file {string} -- Path to the regex rule file

    Returns:
        classifier_type {string} -- The type of classifier that is required by the rule. E.g RegexClassifier, CaptureClassifier etc..
        classifier_args {dictionary} -- A dictionary of arguments that will be used by the classifier
        regexes {dictionary} -- A dictionary that maps the rule to a list of regexes for that rule
    """

    regexes = {}

    # TODO: Check if tuple unpacking like this is an issue

    if regex_file.endswith(".txt"):
        classifier_type, classifier_args, class_name, regexes[class_name] = \
            di.regexes_from_csv(regex_file, use_custom_score=True)
    else:
        classifier_type = None
        classifier_args = {}
        for pack in di.regexes_from_json2(regex_file, use_custom_score=True):
            classifier_type, classifier_args, class_name, regexes[class_name] = pack

    classifier_type = "RegexClassifier" if not classifier_type else classifier_type

    return classifier_type, classifier_args, regexes


def import_regexes(regex_directory):
    """Import multiple regex rule files which will be used in multiclass classification

    Arguments:
        regex_directory {string} -- Path to the directory which contains the rule files for a category e.g smoking status

    Returns:
        classifier_type {string} -- The type of classifier that is required by the rule. E.g RegexClassifier, CaptureClassifier etc..
        classifier_args {dictionary} -- A dictionary of arguments that will be used by the classifier
        regexes {dictionary} -- A dictionary that maps the rule to a list of regexes for that rule
    """
    file_names = os.listdir(regex_directory)
    regex_filenames = [os.path.join(regex_directory, fname) for fname in file_names]

    regexes = {}

    classifier_type = None
    classifier_args = {}

    for file in regex_filenames:
        if file.endswith(".txt"):
            _classifier_type, _classifier_args, _class_name, regexes[_class_name] = \
                di.regexes_from_csv(file, use_custom_score=True)
        else:
            _classifier_type = None
            _classifier_args = {}
            for pack in di.regexes_from_json2(file, use_custom_score=True):
                _classifier_type, _classifier_args, _class_name, regexes[_class_name] = pack

        classifier_type = _classifier_type if _classifier_type else classifier_type
        classifier_args = _classifier_args if _classifier_args else classifier_args

    classifier_type = "RegexClassifier" if not classifier_type else classifier_type

    return classifier_type, classifier_args, regexes


def import_regexes2(regexes_directory):
    file_names = os.listdir(regexes_directory)
    regex_filenames = [os.path.join(regexes_directory, fname) for fname in file_names if fname.endswith(".txt")]
    regexes = {}

    for file in regex_filenames:
        _, _, _class_name, regexes[_class_name] = di.regexes_from_csv(file, use_custom_score=True)

    if "rule_settings.json" not in file_names:
        classifier_args = {}
        classifier_type = "RegexClassifier"
    else:
        classifier_type, classifier_args = di.read_classifier_settings(os.path.join(regexes_directory,
                                                                                    "rule_settings.json"))

    return classifier_type, classifier_args, regexes

def import_regexes3(regexes_directory, mode="advanced"):
    file_names = os.listdir(regexes_directory)
    settings_files = ["rule_settings.json", "rule_properties.json"]

    ext = ".txt" if mode=="advanced" else ".json"
    
    regex_filenames = [fname for fname in file_names if fname.endswith(ext) and fname not in settings_files]

    regex_filenames = [os.path.join(regexes_directory, fname) for fname in regex_filenames]

    regexes = {}

    for file in regex_filenames:
        _class_name, regexes[_class_name] = di.regexes_from_csv(file, use_custom_score=True) if file.endswith(".txt")\
            else di.regexes_from_json(file, use_custom_score=True)

    if "rule_settings.json" not in file_names:
        classifier_args = {}
        classifier_type = "RegexClassifier"
    else:
        classifier_type, classifier_args = di.read_classifier_settings(os.path.join(regexes_directory,
                                                                                    "rule_settings.json"))

    return classifier_type, classifier_args, regexes


def get_rule_properties(rule_path, rule_name, pwds=None):
    file_name = os.path.join(rule_path, "rule_properties.json")

    if "rule_properties.json" not in os.listdir(rule_path):
        label_col = 1
        label_func = None
        classifier_runtime_args = {}
        classifier_initialization_args = None
    else:
        with open(file_name) as j:
            data = json.load(j)

        label_col = data["Label Col"] if "Label Col" in data else 1

        required_pwds = data["Pwds"] if "Pwds" in data else None
        cur_pwds = {pwd_name: pwds[pwd_name] for pwd_name in data["Pwds"]} if "Pwds" in data else None

        use_preprocessor = False if ("Use Preprocessor" not in data or not data["Use Preprocessor"]) else True
        preprocessor = PwdPreprocessor2(pwds, required_pwds, to_lower=True) if use_preprocessor else None

        classifier_runtime_args = {"pwds": cur_pwds,
                                   "preprocess_func": preprocessor.preprocess if preprocessor else None}
        classifier_initialization_args = None

        use_python = False if ("Specify Function with Python" not in data or not data["Specify Function with Python"]) \
            else True

        label_func = None

        if use_python:
            settings_dict = {}
            if "python_settings.py" in os.listdir(rule_path):
                settings_dict = settings_factory(os.path.join(rule_path, "python_settings.py"))
            else:
                if rule_name not in file_to_args:
                    print("Rule not found in custom python function")
                else:
                    settings_dict = file_to_args[rule_name]

            if "Runtime Params" in settings_dict:
                classifier_runtime_args.update(settings_dict["Runtime Params"])

            if "Runner Initialization Params" in settings_dict:
                label_func = settings_dict["Runner Initialization Params"]["label_func"] \
                    if "label_func" in settings_dict["Runner Initialization Params"] else None

                classifier_initialization_args = {key: settings_dict["Runner Initialization Params"][key]
                                                  for key in settings_dict["Runner Initialization Params"]
                                                  if key != "label_func"}

    return label_col, label_func, classifier_runtime_args, classifier_initialization_args


