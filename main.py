from variable_classifiers.base_runner import Runner, import_regexes, import_regex
from datahandler import data_import as di
import os
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', "--repeat_ids", help="Ids are unique and only the latest instance of the data corresponding to that id is used. (default: Appends data instances for corresponding id)", action="store_true")
    parser.add_argument('-t', "--training_mode", action='store', nargs=5, metavar=('id_cols', 'label_cols', 'first_row', 'label_file', 'train_percent'),
                        help="Puts the classifier into training mode with specified ratio of training examples. (default: 0.6)")
    parser.add_argument('filename',  help='A .csv or .xlsx file which contains a column containing patient ids and a column containing patient data (string of text)')
    parser.add_argument('rules_folder',  help='A folder containing a list of rule files (.txt) or a folder of rules in the case of multiclass classification')
    parser.add_argument('data_col',  help='The column which hosts the data instances. Starts counting at 1 for .xlsx files and 0 for .csv files', type=int)
    parser.add_argument('id_col',  help='The column which hosts the id instances. Starts counting at 1 for .xlsx files and 0 for .csv files', type=int)
    parser.add_argument('line_start',  help='The row at which to start  reading the ids and the data')
    args = parser.parse_args()

    filename = args.filename
    rules = args.rules_folder
    repeat_ids = args.repeat_ids
    data_col = args.data_col
    id_col = args.id_col
    line_start = args.line_start
    training_mode = None if not args.training_mode else args.training_mode
    train=False
    print(training_mode)

    if repeat_ids:
        print("Only using most recent patient data")

    data, _, ids = di.data_from_csv([filename], data_cols=data_col, id_cols=id_col, repeat_ids=repeat_ids) if filename.endswith('.csv')\
        else di.data_from_excel([filename], data_cols=data_col, id_cols=id_col, repeat_ids=repeat_ids)

    if training_mode:
        l_id_col = int(training_mode[0])
        l_label_col = int(training_mode[1])
        l_first_row = int(training_mode[2])
        label_file = training_mode[3]
        train_percent = float(training_mode[4])
        train = True

        _, temp_labels, temp_ids = di.data_from_excel([label_file], id_cols=l_id_col, label_cols=l_label_col, repeat_ids=repeat_ids, first_row=l_first_row, check_col=1)

        labels = ["None"] * len(data)
        count = 0
        for i, data_id in enumerate(ids):
            if data_id in temp_ids:
                labels[i] = temp_labels[temp_ids.index(data_id)]
            else:
                count += 1

    rule_list = []
    classifiers = []
    classifiers_args = []

    rules = [(fname, os.path.join(rules, fname)) for fname in os.listdir(rules)]
    print(rules)

    for rule_name, rule in rules:
        classifier_type, classifier_args, regexes_dict = import_regexes(rule) if os.path.isdir(rule) else import_regex(rule)
        classifier_args.update({"regexes": regexes_dict})
        classifiers_args.append(classifier_args)
        classifiers.append(classifier_type)

    # classifiers_args_list = [{"", "classifier_name"}]

    for classifier_args, classifier in zip(classifiers_args, classifiers):
        rule_classifier = Runner(classifier, **classifier_args)

        if not train:
            rule_classifier.run(ids=ids, data=data)
        else:
            rule_classifier.run(ids=ids, data=data, labels=labels, train=train, train_percent=train_percent)

        print(rule_classifier.classifier.dataset["test"]["preds"])

    # data_filenames = [os.path.normpath(os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Cohort 2 (really cleansed).csv'))]
    # data, _, ids = di.data_from_csv(data_filenames, data_cols=2, id_cols=0, repeat_ids=False)
    # regex_dir = os.path.join('examples', 'regexes', 'tb_regexes', 'smoking_new')
    #
    # regexes = import_regexes(regex_dir)
    # regex_biases = {regex_name: (0 if regex_name is not "None" else 1) for regex_name in regexes}
