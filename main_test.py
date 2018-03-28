#MAIN RUNNING CODE
from variable_classifiers.base_runner import Runner
from datahandler import data_import as di
from datahandler import data_export as de
import os

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
    classifier_type, classifier_args, class_name, regexes[class_name] = di.regexes_from_csv(regex_file, use_custom_score=True)

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
        _classifier_type, _classifier_args, _class_name, regexes[_class_name] = di.regexes_from_csv(file, use_custom_score=True)
        classifier_type = _classifier_type if _classifier_type else classifier_type
        classifier_args = _classifier_args if _classifier_args else classifier_args

    classifier_type = "RegexClassifier" if not classifier_type else classifier_type

    return classifier_type, classifier_args, regexes

def create_regex_based_classifier(rule_path, ids, data, labels=None, training_mode=False, l_id_col=None, l_label_col=None, l_first_row=None, label_file=None, repeat_ids=False, train_percent=0.6):
    """Creates a Regex based classifier Runner object which is later used to run the classifier
    
    Arguments:
        rule_path {String} -- Path to the rule directory (in the case of multiclass classification) or a rule file (in the case of single class classificatoin)
        ids {list} -- List of ids
        data {list} -- List of data (string) for each id
    
    Keyword Arguments:
        labels {list} -- List of labels (default: {None})
        training_mode {bool} -- Whether to run the classifier in training mode. If in training mode creates training and validation datasets (default: {False})
        l_id_col {int} -- Column in which label_file's ids are located (default: {None})
        l_label_col {int} -- Column in which label_file's labels are located (default: {None})
        l_first_row {int} -- From which row to start reading the data (default: {None})
        label_file {String} -- Path pointing to label file (default: {None})
        repeat_ids {bool} -- If False, ids are not considered unique and the data is appended (default: {False})
        train_percent {float} -- Percentage of training examples (default: {0.6})
    
    Returns:
        classifier_runner {Runner} -- Returns a Runner object which is used to run the classifier
    """

    #Import rule directory or rule file and updating classifier_args
    #Creating the Runner object with specified classifier_args
    classifier_type, classifier_args, regexes_dict = import_regexes(rule_path) if os.path.isdir(rule_path) else import_regex(rule_path)
    classifier_args.update({"regexes": regexes_dict})
    classifier_runner = Runner(classifier_type, **classifier_args)

    #If training is enabled
    if training_mode:
        #If a label_file was specified, read the labels from the file
        if label_file:
            dataloader = di.data_from_csv if label_file.endswith('.csv') else di.data_from_excel
            _, temp_labels, temp_ids = dataloader([label_file], id_cols=l_id_col, label_cols=l_label_col, repeat_ids=repeat_ids, first_row=l_first_row, check_col=1)

            labels = ["None"] * len(data)
            for i, data_id in enumerate(ids):
                if data_id in temp_ids:
                    labels[i] = temp_labels[temp_ids.index(data_id)]

        #Storing data within classifier and creating validation and training sets
        classifier_runner.classifier.import_data(data=data, labels=labels, ids=ids)
        classifier_runner.classifier.create_train_and_valid(train_percent=train_percent)

    #Otherwise, just load it into test
    else:
        classifier_runner.classifier.load_dataset("test", data=data, ids=ids)

    return classifier_runner

if __name__ == "__main__":
        debug=False

        #Setup code
        pwds = di.import_pwds([os.path.join("dictionaries", dict_name) for dict_name in os.listdir("dictionaries")])
        filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Cohort 2 (really cleansed).csv')
        label_filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx')
        rules_path = os.path.join(os.getenv('TB_DATA_FOLDER'), 'rules')
        dummy_rules_path = os.path.join(*["examples", "regexes", "tb_regexes"])

        #loading data
        if not debug:
            dataloader = di.data_from_csv if filename.endswith('.csv') else di.data_from_excel
            data, _, ids = dataloader([filename], data_cols=2, first_row=1, id_cols=0, repeat_ids=False)
        else: 
            data = ["She migrated from Trinidad in 1999", "He immigrated from the US in 1920. He moved to Canada in 1920", "He is Canadian."]
            labels = ["Trinidad", "US", "Canada"]
            ids = ["0", "1", "2"]


        all_classifications = []
        all_classifications.append(ids)
        excel_column_headers = ["Ids", "Smoking Status", "Immigration Year"]

        #Creating and running smoking classifier
        smoking_rules = os.path.join(rules_path, 'smoking_new')
        # smoking_classifier = create_regex_based_classifier(smoking_rules, ids, data, training_mode=True, l_id_col=1, l_label_col=7, l_first_row=2, label_file=label_filename)
        smoking_classifier = create_regex_based_classifier(smoking_rules, ids, data)
        smoking_classifier.run(datasets=["test"])
        # all_classifications.append(smoking_classifier.classifier.dataset["test"]["preds"].tolist())

        #Dictionary mapping from ethnicity to country
        ethnicity_to_country = {ethnicity: country for country,ethnicity in zip(pwds["country"],pwds["ethnicity"])}

        #Convert the captured ethnicity into a country
        def country_capture_convert(capture):
            if capture in ethnicity_to_country:
                return ethnicity_to_country[capture]

            return capture

        #Creating and running immigration classifier
        immigration_rules = os.path.join(dummy_rules_path, "immigration_country.txt")
        # immigration_classifier = create_regex_based_classifier(immigration_rules, ids, data, labels, training_mode=True)
        immigration_classifier = create_regex_based_classifier(immigration_rules, ids, data)
        #Passing in the personal word dictionaries and labelling function
        immigration_classifier.run(datasets=["test"], pwds=pwds, label_func=country_capture_convert)
        # all_classifications.append(immigration_classifier.classifier.dataset["test"]["preds"].tolist())

        ####################################################################################################
        #WIP - example run on all tbs
        #Note - tb country functionality not implemented. Will do later
        ####################################################################################################

        tb_rules = os.path.join(rules_path, "tb")

        for rule in os.listdir(tb_rules):
            print(rule)
            rule_file = os.path.join(tb_rules, rule)
            classifier_runner = create_regex_based_classifier(rule_file, ids, data)
            classifier_runner.run(datasets=["test"], pwds=pwds)
            all_classifications.append(classifier_runner.classifier.dataset["test"]["preds"].tolist())

        de.export_data_to_excel("nlp_chart_extraction_cohort_2.xlsx", all_classifications, excel_column_headers, mode="r")
