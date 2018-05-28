# MAIN RUNNING CODE
from variable_classifiers.base_runner import Runner
import numpy as np
from web.report_generator import generate_error_report
from stats.basic import calculate_accuracy
from sklearn.metrics import confusion_matrix
from stats.basic import plot_confusion_matrix, get_classification_stats, compute_ppv_accuracy_ova, \
    compute_ppv_accuracy_capture, get_classification_stats_capture
from datahandler.helpers import import_regex, import_regexes
from properties import *

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


if __name__ == "__main__":
    # loading data
    if not debug:
        pass
    else:
        repeated_data_list = None
        data_list = ["She migrated from Trinidad in 1999",
                     "He immigrated from the US in 1920. He moved to Canada in 1920", "He is Canadian."]
        labels = ["Trinidad", "US", "Canada"]
        ids_list = ["0", "1", "2"]

    # TODO: Update Headers
    datasets = ["train", "valid"]

    # cur_run = file_to_args.keys()
    # cur_run = ["country.txt"]
    # cur_run = ["inh_medication.txt", "pyrazinamide_medication.txt", "rifampin_medication.txt",
    # "ethambutol_medication.txt","rifabutin_medication.txt", "moxifloxacin_medication.txt", "rifapentine_medication.txt",
    #  "capreomycin_medication.txt", "amikacin_medication.txt", "pas_medication.txt", "cycloserine_medication.txt",
    #  "ethionamide_medication.txt", "vitamin_b6_medication.txt"]
    # cur_run = ["hcw", "smh", "inh_medication.txt", "corticosteroids_immuno", "chemotherapy_immuno", "TNF_immuno"]
    # cur_run = ["afb_positive.txt", "disseminated.txt", "extra_pulmonary.txt"]
    # cur_run = ["smoking_new"]

    # cur_run = ["corticosteroids_immuno.txt"]
    # cur_run = ["inh_medication_2.txt"]

    cur_run = ["diag_active"]

    # TODO: Add functools label_funcs for some of the classifiers
    # TODO: Use country preprocessor from old code
    row_start = {"train": 29,
                 "valid": 20,
                 "test": 53
                 }

    # excel_column_headers = ["Ids"]
    for rule in cur_run:
        rule_name = rule.split(sep=".txt")[0]

        print("=" * 100)
        rule_file = os.path.join(tb_rules, rule)
        classifier_runner = create_regex_based_classifier(rule_file)
        cur_params = file_to_args[rule]["Runner Initialization Params"]
        if "data_list" not in cur_params:
            cur_params["data_list"] = data_list
        if "ids_list" not in cur_params:
            cur_params["ids_list"] = ids_list

        data = {}
        labels = {}
        ids = {}
        if "label_file" in cur_params:
            data["all"], labels["all"], ids["all"] = di.get_labeled_data(**cur_params)
            classifier_runner = load_classifier_data(classifier_runner, data["all"], labels['all'], ids["all"],
                                                     create_train_valid=True, train_percent=.6, random_seed=0)
        else:
            for cur_dataset in datasets:
                if "use_row_start" in file_to_args[rule]:
                    cur_params['l_first_row'] = row_start[cur_dataset]
                cur_params["label_file"] = label_files_dict[cur_dataset]
                data[cur_dataset], labels[cur_dataset], ids[cur_dataset] = di.get_labeled_data(**cur_params)
                classifier_runner = load_classifier_data(classifier_runner, data[cur_dataset], labels[cur_dataset],
                                                         ids[cur_dataset], dataset=cur_dataset)
        for cur_dataset in datasets:
            all_classifications = []
            print("\nRunning on rule: {} - {}".format(rule_name, cur_dataset))

            # classifier_runner.classifier.dataset[cur_dataset]["ids"] = [classifier_runner.classifier.dataset[cur_dataset]["ids"][2]]
            # classifier_runner.classifier.dataset[cur_dataset]["data"] = [classifier_runner.classifier.dataset[cur_dataset]["data"][2]]
            if "Runtime Params" in file_to_args[rule]:
                classifier_runner.run(datasets=[cur_dataset], **file_to_args[rule]["Runtime Params"])
            else:
                classifier_runner.run(datasets=[cur_dataset])

            failures_dict = {}

            cur_labels_list = sorted(list(set(classifier_runner.classifier.dataset[cur_dataset]["preds"].tolist()) |
                                          set(classifier_runner.classifier.dataset[cur_dataset]["labels"].tolist())))
            accuracy, \
                incorrect_indices = calculate_accuracy(classifier_runner.classifier.dataset[cur_dataset]["preds"],
                                                       classifier_runner.classifier.dataset[cur_dataset]["labels"])

            print("\nAccuracy: ", accuracy)
            print("\nIds: ", classifier_runner.classifier.dataset[cur_dataset]["ids"])
            print("Predictions: ", classifier_runner.classifier.dataset[cur_dataset]["preds"])
            print("Labels: ", classifier_runner.classifier.dataset[cur_dataset]["labels"])

            print("\nIncorrect Ids: ", classifier_runner.classifier.dataset[cur_dataset]["ids"][incorrect_indices])
            print("Incorrect Predictions: ",
                  classifier_runner.classifier.dataset[cur_dataset]["preds"][incorrect_indices])
            print("Incorrect Labels: ", classifier_runner.classifier.dataset[cur_dataset]["labels"][incorrect_indices])

            classifier_type = classifier_runner.classifier_type.__name__

            if classifier_type == "CaptureClassifier":
                cnf_matrix = None

                classifier_classes = sorted(list(classifier_runner.classifier_parameters["regexes"]))

                ppv_and_accuracy = compute_ppv_accuracy_capture(
                    classifier_runner.classifier.dataset[cur_dataset]["labels"],
                    classifier_runner.classifier.dataset[cur_dataset]["preds"],
                    classifier_classes, classifier_runner.classifier.negative_label)

                predicted_positive, positive_cases, predicted_negative_cases, negative_cases, \
                false_positives, false_negatives = get_classification_stats_capture(
                    classifier_runner.classifier.dataset[cur_dataset]["labels"],
                    classifier_runner.classifier.dataset[cur_dataset]["preds"],
                    classifier_classes, classifier_runner.classifier.negative_label)

                cur_labels_list = classifier_classes

            else:

                cnf_matrix = confusion_matrix(classifier_runner.classifier.dataset[cur_dataset]["labels"],
                                              classifier_runner.classifier.dataset[cur_dataset]["preds"])
                ppv_and_accuracy = compute_ppv_accuracy_ova(cnf_matrix, cur_labels_list)
                predicted_positive, positive_cases, predicted_negative_cases, negative_cases, \
                false_positives, false_negatives = get_classification_stats(cnf_matrix, cur_labels_list)

            print("Confusion Matrix: ")

            print("OVA PPV and Accuracy: ", ppv_and_accuracy)

            print("Number of Positive Predictions: ", predicted_positive)
            print("Actual number of Positive Cases: ", positive_cases)
            print("Number of Predicted Negative Cases: ", predicted_negative_cases)
            print("Actual Number of Negative Cases: ", negative_cases)

            for index in incorrect_indices:
                cur_patient_id = classifier_runner.classifier.dataset[cur_dataset]["ids"][index]
                cur_pred = classifier_runner.classifier.dataset[cur_dataset]["preds"][index]
                cur_label = classifier_runner.classifier.dataset[cur_dataset]["labels"][index]
                cur_match_obj = classifier_runner.classifier.dataset[cur_dataset]["matches"][index]
                cur_score = classifier_runner.classifier.dataset[cur_dataset]["scores"][index]
                cur_text = classifier_runner.classifier.dataset[cur_dataset]["data"][index]

                failures_dict[cur_patient_id] = {"label": cur_label, "data": cur_text, "pred": cur_pred,
                                                 "matches": cur_match_obj, "score": cur_score}

            if not all_classifications:
                all_classifications.append(classifier_runner.classifier.dataset[cur_dataset]["ids"].tolist())

            all_classifications.append(classifier_runner.classifier.dataset[cur_dataset]["preds"].tolist())

            if cur_dataset != "test":
                all_classifications.append(classifier_runner.classifier.dataset[cur_dataset]["labels"].tolist())

            # excel_column_headers.append(file_to_header[rule])
            # excel_column_headers.append("Label")

            gen_path = os.path.join("generated_data", rule_name, cur_dataset)

            if not os.path.exists(gen_path):
                os.makedirs(gen_path)

            # TODO: FIX STAT CREATION FOR CAPTURE CLASSIFIERS
            error_data = {"Predicted Positive": predicted_positive, "Positive Cases": positive_cases,
                          "Predicted Negative": predicted_negative_cases, "Negative Cases": negative_cases,
                          "False Positives": false_positives, "False Negatives": false_negatives,
                          "Confusion Matrix": cnf_matrix.tolist() if cnf_matrix is not None else [],
                          "OVA PPV and Accuracy": ppv_and_accuracy, "Ordered Labels": cur_labels_list,
                          "Negative Label": classifier_runner.classifier.negative_label,
                          "Classifier Type": classifier_type}


            custom_class_colours = None

            if len(classifier_classes) == 2:
                negative_label = classifier_runner.classifier.negative_label
                positive_label = next(filter(lambda i: i != negative_label, classifier_classes))
                custom_class_colours = {negative_label: "hsl({},{}%,{}%)".format(15,71.4,89),
                                        positive_label: "hsl({},{}%,{}%)".format(97,81,91.8)}

            generate_error_report(os.path.join("generated_data", rule_name, cur_dataset),
                                  template_directory, "{}".format(rule_name),
                                  classifier_runner.classifier.regexes.keys(), failures_dict, effects,
                                  custom_effect_colours=effect_colours, addition_json_params=error_data,
                                  custom_class_colours=custom_class_colours)

            headers = ["ID", "Prediction", "Actual"]
            excel_path = os.path.join("generated_data", rule_name, cur_dataset, rule_name)
            conf_path = os.path.join("generated_data", rule_name, cur_dataset)

            if cnf_matrix is not None:
                plot_confusion_matrix(cnf_matrix, cur_labels_list, conf_path)

            # de.export_data_to_excel("{}.xlsx".format(excel_path), all_classifications, headers, mode="r")
