#MAIN RUNNING CODE
from variable_classifiers.base_runner import Runner
from datahandler import data_import as di
from datahandler import data_export as de
import functools
import os
from web.report_generator import generate_error_report
from stats.basic import calculate_accuracy
from sklearn.metrics import confusion_matrix
from stats.basic import plot_confusion_matrix, get_classification_stats, compute_ppv_accuracy_ova
from datahandler.helpers import import_regex, import_regexes
from datahandler.preprocessors import replace_labels_with_required,replace_label_with_required, replace_filter, convert_repeated_data_to_sublist
from classifier.classification_functions import sputum_classify


def create_regex_based_classifier(rule_path=None, ids_list=None, data_list=None, labels_list=None, training_mode=False, l_id_col=1, l_label_col=None, l_first_row=2, label_file=None, repeat_ids=False, train_percent=0.6, label_func=None):
    """Creates a Regex based classifier Runner object which is later used to run the classifier
    
    Arguments:
        rule_path {String} -- Path to the rule directory (in the case of multiclass classification) or a rule file (in the case of single class classificatoin)
        ids_list {list} -- List of ids
        data_list {list} -- List of data (string) for each id
    
    Keyword Arguments:
        labels_list {list} -- List of labels (default: {None})
        training_mode {bool} -- Whether to run the classifier in training mode. If in training mode creates training and validation datasets (default: {False})
        l_id_col {int} -- Column in which label_file's ids are located starting from 0 (default: {None})
        l_label_col {int} -- Column in which label_file's labels are located starting from 0 (default: {None})
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
            #TODO: accordingly increment/decrement l_id_col, l_label_col, l_first_row, check_col depending on filetype
            _, temp_labels, temp_ids = dataloader([label_file], id_cols=l_id_col, label_cols=l_label_col, repeat_ids=repeat_ids, first_row=l_first_row, check_col=1)

            labels_list = ["None"] * len(data_list)
            for i, data_id in enumerate(ids_list):
                if data_id in temp_ids:
                    labels_list[i] = temp_labels[temp_ids.index(data_id)]

            if label_func:
                label_func(labels_list)

        #Storing data within classifier and creating validation and training sets
        classifier_runner.classifier.import_data(data=data_list, labels=labels_list, ids=ids_list)
        train_ids, valid_ids = classifier_runner.classifier.create_train_and_valid(train_percent=train_percent, random_seed=0)

    #Otherwise, just load it into test
    else:
        classifier_runner.classifier.load_dataset("test", data=data_list, ids=ids_list)

    return classifier_runner

if __name__ == "__main__":
        debug = False

        print_none = False
        print_minimal = False
        print_verbose = False

        # Web setup
        template_directory = os.path.join('web', 'templates')
        effects = ["a", "aa", "ab", "r", "rb", "ra"]
        effect_colours = dict.fromkeys(["a", "aa", "ab"], "rgb(0,0,256)")
        effect_colours.update(dict.fromkeys(["r", "rb", "ra"], "rgb(256,0,0)"))

        #Setup code
        pwds = di.import_pwds([os.path.join("dictionaries", dict_name) for dict_name in os.listdir("dictionaries")])
        filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Cohort 2 (really cleansed).csv')
        label_filename2 = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Dev Labelling Decisions', 'labelling_decisions_cohort_2-s.xlsx')
        label_filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx')
        rules_path = os.path.join(os.getenv('TB_DATA_FOLDER'), 'rules')
        dummy_rules_path = os.path.join(*["examples", "regexes", "tb_regexes"])

        #loading data
        if not debug:
            dataloader = di.data_from_csv if filename.endswith('.csv') else di.data_from_excel
            data, _, ids = dataloader([filename], data_cols=2, first_row=1, id_cols=0, repeat_ids=False)
            data_repeated, _, ids_repeated = dataloader([filename], data_cols=2, first_row=1, id_cols=0, repeat_ids=True)
            _, repeated_data_list, repeated_labels_list = convert_repeated_data_to_sublist(ids_repeated, repeated_data=data_repeated)
        else:
            data = ["She migrated from Trinidad in 1999", "He immigrated from the US in 1920. He moved to Canada in 1920", "He is Canadian."]
            labels = ["Trinidad", "US", "Canada"]
            ids = ["0", "1", "2"]

        if not print_none and print_verbose:
            for data_repeated, id_repeated in zip(data_repeated, ids_repeated):
                print("="*100)
                print(id_repeated)
                print(data_repeated)

        #TODO: Update Headers

        tb_rules = os.path.join(rules_path, "tb_rules")
        file_to_header = {"smoking_new": "Smoking Status", "country.txt": "Country of Birth", "diag_active.txt": "Active TB Diagnosis",
                              "diag_ltbi.txt": "LTBI Diagnosis", "diag_method_clinical.txt": "Method of Diagnosis Clinical",
                              "diag_method_culture.txt": "Method of Diagnosis Culture", "diag_method_pcr.txt": "Method of Diagnosis PCR",
                              "diag_ntm.txt": "NTM Diagnosis", "hiv_negative.txt": "Hiv Status Negative", "hiv_positive.txt": "Hiv Status Positive",
                              "hiv_not_dictated.txt":"Hiv Status Not Dictated", "hiv_unknown.txt":"Hiv Status Unknown", "immigration.txt": "Date of Immigration",
                              "sensitivity_full.txt": "Sensitivity Full", "sensitivity_inh.txt": "Sensitivity INH", "sputum_conversion.txt": "Sputum Conversion date",
                              "tb_contact.txt": "TB Contact History", "tb_old.txt": "Old TB"}

        file_to_header = {"inh_medication.txt": "INH Medication", "hcw": "Health Care Worker"}

        file_to_args = {"smoking_new": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 7, "label_file": label_filename}},
                        # "country.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 2, "label_file": label_filename}},
                        "diag_active.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 8, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"LTBI": "None"})}},
                        "diag_method_clinical.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 10, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"PCR positive": "None", "Culture positive": "None"})}},
                        "diag_method_culture.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 10, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"PCR positive": "None", "Clinical diagnosis": "None"})}},
                        "diag_method_pcr.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 10, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"Clinical diagnosis": "None", "Culture positive": "None"})}},
                        "diag_ntm.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 9, "label_file": label_filename}},
                        "hiv_negative.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 4, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"Positive": "None", "Unknown": "None"})}},
                        "hiv_positive.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 4, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"Negative": "None", "Unknown": "None"})}},
                        "hiv_not_dictated.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 4, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"Positive": "None", "Unknown": "None", "Negative": "None", "None": "Not dictated"})}},
                        "hiv_unknown.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 4, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"Positive": "None", "Negative": "None"})}},
                        "immigration.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 3, "label_file": label_filename, "label_func": functools.partial(replace_filter, lambda label: label[0:4])}},
                        "sensitivity_full.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 11, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"INH resistant": "None"})}},
                        "sensitivity_inh.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 11, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"Fully sensitive": "None"})}},
                        "sputum_conversion_2": {"Runner Initialization Params": {"ids_list": ids, "data_list": repeated_data_list, "training_mode": True, "l_label_col": 12, "label_file": label_filename, "label_func": functools.partial(replace_filter, lambda label: label[0:4])},
                                                "Runtime Params": {"classify_func": sputum_classify}},
                        "tb_contact.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 5, "label_file": label_filename}},
                        "tb_old.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 6, "label_file": label_filename}},
                        "diag_ltbi.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 8, "label_file": label_filename, "label_func": functools.partial(replace_label_with_required, {"Active TB": "None"})}},
                        "inh_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Isoniazid (INH)", "None"])},
                                                   "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "pyrazinamide_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Pyrazinamide (Z/Pza)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "rifampin_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Rifampin (RIF)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "ethambutol_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Ethambutol (E/Emb)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "rifabutin_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Rifabutin (Rfb)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "moxifloxacin_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Moxifloxacin (Mfx)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "rifapentine_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Rifapentine (RPT)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "capreomycin_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Capreomycin (Cm)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "amikacin_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Amikacin (Amk)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "pas_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Para-aminosalicylic acid (Pas)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "cycloserine_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Cycloserine (Dcs)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "ethionamide_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Ethionamide (Eto)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "vitamin_b6_medication.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": [13,14,15,16,17], "label_file": label_filename, "label_func": functools.partial(replace_labels_with_required, *["Vitamin B6", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "hcw": {"Runner Initialization Params": {"training_mode": True, "l_id_col": 0, "l_label_col": 1, "label_file": label_filename2},
                                                   "Runtime Params": {"label_func": None, "pwds": pwds}},
                        "corticosteroids_immuno": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 21, "label_file": label_filename,
                                                                                    "label_func": functools.partial(replace_label_with_required, {"Corticosteroids (prednisone)": "Yes",
                                                                                                                                                 "Other": "No", 'None': "No", "Chemotherapy": "No", "TNF alpha inhibitors": "No"})}},
                        "chemotherapy_immuno": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 21, "label_file": label_filename,
                                                                                    "label_func": functools.partial(replace_label_with_required, {"Corticosteroids (prednisone)": "No",
                                                                                                                                                 "Other": "No", 'None': "No", "Chemotherapy": "Yes", "TNF alpha inhibitors": "No"})}},
                        "TNF_immuno": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 21, "label_file": label_filename,
                                                                                    "label_func": functools.partial(replace_label_with_required, {"Corticosteroids (prednisone)": "No",
                                                                                                                                                 "Other": "No", 'None': "No", "Chemotherapy": "No", "TNF alpha inhibitors": "Yes"})}},
                        "BCG": {"Runner Initialization Params": {"training_mode": True, "l_id_col": 0, "l_label_col": 7, "label_file": label_filename2}},
                        "smh": {"Runner Initialization Params": {"training_mode": True,"l_id_col": 0,
                                "l_label_col": 3,
                                "label_file": label_filename2,
                                "l_first_row": 1
                                }},
                        "afb_positive.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 25, "label_file": label_filename}},
                        "disseminated.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 25, "label_file": label_filename}},
                        "extra_pulmonary.txt": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 25, "label_file": label_filename}},
                        "other_tb_risk_factors": {"Runner Initialization Params": {"training_mode": True, "l_label_col": 23, "label_file": label_filename}}}

        datasets = ["train"]

        # cur_run = file_to_args.keys()
        cur_run = ["sputum_conversion_2"]
        # cur_run = ["hcw", "smh", "inh_medication.txt", "corticosteroids_immuno", "chemotherapy_immuno", "TNF_immuno", "BCG"]
        # cur_run = ["afb_positive.txt", "disseminated.txt", "extra_pulmonary.txt", "immigration.txt"]
        # cur_run = ["hcw", "smh"]
        # cur_run = ["other_tb_risk_factors"]

        #TODO: Add functools label_funcs for some of the classifiers
        #TODO: Use country preprocessor from old code

        for dataset in datasets:
            excel_column_headers = ["Ids"]
            for rule in cur_run:
                all_classifications = []
                rulename = rule.split(sep=".txt")[0]

                print("="*100)
                print("\nRunning on rule: {} - {}".format(rulename, dataset))
                rule_file = os.path.join(tb_rules, rule)

                if "data_list" and "ids_list" not in file_to_args[rule]["Runner Initialization Params"]:
                    classifier_runner = create_regex_based_classifier(rule_file, ids, data, **file_to_args[rule]["Runner Initialization Params"])
                else:
                    classifier_runner = create_regex_based_classifier(rule_file, **file_to_args[rule]["Runner Initialization Params"])

                if "Runtime Params" in file_to_args[rule]:
                    classifier_runner.run(datasets=[dataset], **file_to_args[rule]["Runtime Params"])
                else:
                    classifier_runner.run(datasets=[dataset])
                accuracy, incorrect_indices = calculate_accuracy(classifier_runner.classifier.dataset[dataset]["preds"],
                                                                 classifier_runner.classifier.dataset[dataset]["labels"])


                cnf_matrix = confusion_matrix(classifier_runner.classifier.dataset[dataset]["labels"], classifier_runner.classifier.dataset[dataset]["preds"])
                labels_list = sorted(list(set(classifier_runner.classifier.dataset[dataset]["preds"].tolist()) | set(classifier_runner.classifier.dataset[dataset]["labels"].tolist())))

                print("\nIds: ", classifier_runner.classifier.dataset[dataset]["ids"])
                print("Predictions: ", classifier_runner.classifier.dataset[dataset]["preds"])
                print("Labels: ", classifier_runner.classifier.dataset[dataset]["labels"])
                failures_dict = {}

                print("\nAccuracy: ", accuracy)

                print("Confusion Matrix: ")
                print(cnf_matrix)

                ppv_and_accuracy = compute_ppv_accuracy_ova(cnf_matrix, labels_list)
                predicted_positive, positive_cases, predicted_negative_cases, negative_cases, false_positives, false_negatives = get_classification_stats(cnf_matrix, labels_list)

                print("OVA PPV and Accuracy: ", ppv_and_accuracy)

                print("Number of Positive Predictions: ", predicted_positive)
                print("Actual number of Positive Cases: ", positive_cases)
                print("Number of Predicted Negative Cases: ", predicted_negative_cases)
                print("Actual Number of Negative Cases: ", negative_cases)

                for index in incorrect_indices:
                    patient_id = classifier_runner.classifier.dataset[dataset]["ids"][index]
                    pred = classifier_runner.classifier.dataset[dataset]["preds"][index]
                    label = classifier_runner.classifier.dataset[dataset]["labels"][index]
                    match_obj = classifier_runner.classifier.dataset[dataset]["matches"][index]
                    score = classifier_runner.classifier.dataset[dataset]["scores"][index]
                    text = classifier_runner.classifier.dataset[dataset]["data"][index]

                    failures_dict[patient_id] = {"label": label, "data": text, "pred": pred, "matches": match_obj,
                                                 "score": score}

                print("\nIncorrect Ids: ", classifier_runner.classifier.dataset[dataset]["ids"][incorrect_indices])
                print("Incorrect Predictions: ", classifier_runner.classifier.dataset[dataset]["preds"][incorrect_indices])
                print("Incorrect Labels: ", classifier_runner.classifier.dataset[dataset]["labels"][incorrect_indices])

                if not all_classifications:
                    all_classifications.append(classifier_runner.classifier.dataset[dataset]["ids"].tolist())

                all_classifications.append(classifier_runner.classifier.dataset[dataset]["preds"].tolist())

                if dataset != "test":
                    all_classifications.append(classifier_runner.classifier.dataset[dataset]["labels"].tolist())

                # excel_column_headers.append(file_to_header[rule])
                # excel_column_headers.append("Label")
                if not os.path.exists(os.path.join("generated_data", rulename, dataset)):
                    os.makedirs(os.path.join("generated_data", rulename, dataset))

                #TODO: FIX STAT CREATION FOR CAPTURE CLASSIFIERS
                error_data = {"Predicted Positive": predicted_positive, "Positive Cases": positive_cases, "Predicted Negative": predicted_negative_cases,
                              "Negative Cases": negative_cases, "False Positives": false_positives, "False Negatives": false_negatives,
                              "Confusion Matrix": cnf_matrix.tolist(), "OVA PPV and Accuracy": ppv_and_accuracy, "Ordered Labels": labels_list}

                print(ppv_and_accuracy)

                generate_error_report(os.path.join("generated_data", rulename, dataset),template_directory, "{}".format(rulename),
                                      classifier_runner.classifier.regexes.keys(), failures_dict, effects,
                                      custom_effect_colours=effect_colours, addition_json_params=error_data)

                '''
                generate_error_report(os.path.join("generated_data", rulename, dataset),
                                      "{}_error_report.html".format(rulename), template_directory, 'error_report.html',
                                      "{}".format(rulename), classifier_runner.classifier.regexes.keys(), failures_dict,
                                      effects, custom_effect_colours=effect_colours)
                '''
                headers = ["ID", "Prediction", "Actual"]
                excel_path = os.path.join("generated_data", rulename, dataset, rulename)
                conf_path = os.path.join("generated_data", rulename, dataset)
                plot_confusion_matrix(cnf_matrix, labels_list, conf_path)
                #de.export_data_to_excel("{}.xlsx".format(excel_path), all_classifications, headers, mode="r")

