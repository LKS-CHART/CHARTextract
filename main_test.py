from variable_classifiers.base_runner import Runner
from datahandler import data_import as di
import os

def import_regex(regex_file):

    regexes = {}

    classifier_type, classifier_args, class_name, regexes[class_name] = di.regexes_from_csv(regex_file, use_custom_score=True)

    classifier_type = "RegexClassifier" if not classifier_type else classifier_type

    return classifier_type, classifier_args, regexes

def import_regexes(regex_directory):
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

def create_classifier(rule_path, ids, data, training_mode=False, l_id_col=None, l_label_col=None, l_first_row=None, label_file=None, repeat_ids=False, train_percent=0.6):
    classifier_type, classifier_args, regexes_dict = import_regexes(rule_path) if os.path.isdir(rule_path) else import_regex(rule_path)
    classifier_args.update({"regexes": regexes_dict})
    classifier_runner = Runner(classifier_type, **classifier_args)

    if training_mode:
        _, temp_labels, temp_ids = di.data_from_excel([label_file], id_cols=l_id_col, label_cols=l_label_col, repeat_ids=repeat_ids, first_row=l_first_row, check_col=1)

        labels = ["None"] * len(data)
        for i, data_id in enumerate(ids):
            if data_id in temp_ids:
                labels[i] = temp_labels[temp_ids.index(data_id)]

        classifier_runner.classifier.import_data(data=data, labels=labels, ids=ids)
        classifier_runner.classifier.create_train_and_valid(train_percent=train_percent)

    else:
        classifier_runner.classifier.load_dataset("test", data=data, ids=ids)

    return classifier_runner

if __name__ == "__main__":

        filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Cohort 2 (really cleansed).csv')
        label_filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx')

        data, _, ids = di.data_from_csv([filename], data_cols=2, first_row=1, id_cols=0, repeat_ids=False) if filename.endswith('.csv') \
            else di.data_from_excel([filename], data_cols=3, id_cols=1, repeat_ids=False, first_row=1)

        smoking_rules = os.path.join('regexes', 'tb_regexes', 'smoking_new')
        smoking_classifier = create_classifier(smoking_rules, ids, data, training_mode=True, l_id_col=1, l_label_col=7, l_first_row=2, label_filename=smoking_rules)
        smoking_classifier.run(datasets=["train", "valid"])
