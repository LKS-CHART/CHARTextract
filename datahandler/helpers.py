import os
from datahandler import data_import as di

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

    #TODO: Check if tuple unpacking like this is an issue

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
