import sys
import json

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
from datahandler.preprocessors import replace_filter_by_label, replace_labels_with_required, \
    replace_label_with_required, replace_filter, convert_repeated_data_to_sublist
from classifier.classification_functions import sputum_classify, max_classify, max_month
from util.tb_country import preprocess
from util.pwd_preprocessors import PwdPreprocessor2

import os
import sys
orig_stdout = sys.stdout
f = open(os.devnull, 'w')
sys.stdout = f
os.environ['TB_DATA_FOLDER'] = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev"
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
        runner.classifier.create_train_and_valid(ids=classifier_ids_list, data=classifier_data_list, labels=labels_list,
                                                 train_percent=train_percent, random_seed=random_seed)
    return runner


@exposed_function
def run_variable(variable):
    debug = False

    print_none = False
    print_minimal = False
    print_verbose = False

    # Web setup
    template_directory = os.path.join('web', 'templates')
    effects = ["a", "aa", "ab", "r", "rb", "ra"]
    effect_colours = dict.fromkeys(["a", "aa", "ab"], "rgb(0,0,256)")
    effect_colours.update(dict.fromkeys(["r", "rb", "ra"], "rgb(256,0,0)"))

    # Setup code
    pwds = di.import_pwds([os.path.join("dictionaries", dict_name) for dict_name in os.listdir("dictionaries")])
    immuno_preprocessor = PwdPreprocessor2(pwds, ["corticosteroids"], to_lower=True)

    filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'CombinedData.csv')
    label_filename2 = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Dev Labelling Decisions',
                                   'labelling_decisions_cohort_2-s.xlsx')

    label_filename3 = os.path.join(os.getenv('TB_DATA_FOLDER'),
                                   'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx')

    label_files_dict = dict()
    label_files_dict["train"] = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Train_set_labels.xlsx')
    label_files_dict["valid"] = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Valid_set_labels.xlsx')
    # test_label_filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Test_set_labels.xlsx')

    rules_path = os.path.join(os.getenv('TB_DATA_FOLDER'), 'rules')
    dummy_rules_path = os.path.join(*["examples", "regexes", "tb_regexes"])

    # loading data
    if not debug:
        data_loader = di.data_from_csv if filename.endswith('.csv') else di.data_from_excel
        data_list, _, ids_list = data_loader([filename], data_cols=2, first_row=1, id_cols=0, repeat_ids=False)
        data_repeated, _, ids_repeated = data_loader([filename], data_cols=2, first_row=1, id_cols=0, repeat_ids=True)

        _, repeated_data_list, repeated_labels_list = convert_repeated_data_to_sublist(ids_repeated,
                                                                                       repeated_data=data_repeated)

        if not print_none and print_verbose:
            for data_repeated, id_repeated in zip(data_repeated, ids_repeated):
                print("=" * 100)
                print(id_repeated)
                print(data_repeated)
    else:
        repeated_data_list = None
        data_list = ["She migrated from Trinidad in 1999",
                     "He immigrated from the US in 1920. He moved to Canada in 1920", "He is Canadian."]
        labels = ["Trinidad", "US", "Canada"]
        ids_list = ["0", "1", "2"]

    # TODO: Update Headers
    tb_rules = os.path.join(rules_path, "tb_rules")
    file_to_header = {"smoking_new": "Smoking Status",
                      "country.txt": "Country of Birth",
                      "diag_active.txt": "Active TB Diagnosis",
                      "diag_ltbi.txt": "LTBI Diagnosis",
                      "diag_method_clinical.txt": "Method of Diagnosis Clinical",
                      "diag_method_culture.txt": "Method of Diagnosis Culture",
                      "diag_method_pcr.txt": "Method of Diagnosis PCR",
                      "diag_ntm.txt": "NTM Diagnosis",
                      "hiv_negative.txt": "Hiv Status Negative",
                      "hiv_positive.txt": "Hiv Status Positive",
                      "hiv_not_dictated.txt": "Hiv Status Not Dictated",
                      "hiv_unknown.txt": "Hiv Status Unknown",
                      "immigration.txt": "Date of Immigration",
                      "sensitivity_full.txt": "Sensitivity Full",
                      "sensitivity_inh.txt": "Sensitivity INH",
                      "sputum_conversion.txt": "Sputum Conversion date",
                      "tb_contact.txt": "TB Contact History",
                      "tb_old.txt": "Old TB"}

    file_to_header = {"inh_medication.txt": "INH Medication", "hcw": "Health Care Worker"}

    file_to_args = {"smoking_new": {"Runner Initialization Params": {"l_label_col": 7}},
                    "country.txt": {"Runner Initialization Params": {"l_label_col": 2}, "Runtime Params":
                        {"label_func": None, "preprocess_func": preprocess}},
                    "diagnosis": {"Runner Initialization Params": {"l_label_col": 8}},
                    "diag_active_demo.txt": {"Runner Initialization Params":
                                                 {"l_label_col": 8,
                                                  "label_func": functools.partial(replace_label_with_required,
                                                                                  {"LTBI": "None"})}
                                             },
                    "diag_method_clinical.txt": {"Runner Initialization Params":
                                                     {"l_label_col": 10,
                                                      "label_func": functools.partial(replace_label_with_required,
                                                                                      {"PCR positive": "None",
                                                                                       "Culture positive": "None"})}
                                                 },
                    "diag_method_culture.txt": {"Runner Initialization Params":
                                                    {"l_label_col": 10,
                                                     "label_func": functools.partial(replace_label_with_required,
                                                                                     {"PCR positive": "None",
                                                                                      "Clinical diagnosis": "None"})}
                                                },
                    "diag_method_pcr.txt": {"Runner Initialization Params":
                                                {"l_label_col": 10,
                                                 "label_func": functools.partial(replace_label_with_required,
                                                                                 {"Clinical diagnosis": "None",
                                                                                  "Culture positive": "None"})}
                                            },
                    "diag_ntm.txt": {"Runner Initialization Params": {"l_label_col": 9}},
                    "hiv_negative.txt": {"Runner Initialization Params":
                                             {"l_label_col": 4,
                                              "label_func": functools.partial(replace_label_with_required,
                                                                              {"Positive": "None", "Unknown": "None"})}
                                         },
                    "hiv_positive.txt": {"Runner Initialization Params":
                                             {"l_label_col": 4,
                                              "label_func": functools.partial(replace_label_with_required,
                                                                              {"Negative": "None", "Unknown": "None"})}
                                         },
                    "hiv_not_dictated.txt": {"Runner Initialization Params":
                                                 {"l_label_col": 4,
                                                  "label_func": functools.partial(replace_label_with_required,
                                                                                  {"Positive": "None",
                                                                                   "Unknown": "None",
                                                                                   "Negative": "None",
                                                                                   "None": "Not dictated"})}
                                             },
                    "hiv_unknown.txt": {"Runner Initialization Params":
                                            {"l_label_col": 4,
                                             "label_func": functools.partial(replace_label_with_required,
                                                                             {"Positive": "None", "Negative": "None"})}
                                        },
                    "immigration.txt": {"Runner Initialization Params":
                                            {"l_label_col": 3,
                                             "label_func": functools.partial(replace_filter, lambda label: label[0:4]),
                                             "label_file": label_filename3}
                                        },
                    "sensitivity_full.txt": {"Runner Initialization Params":
                                                 {"l_label_col": 11,
                                                  "label_func": functools.partial(replace_labels_with_required,
                                                                                  *["Fully Sensitive", "None"])},
                                             },
                    "sensitivity_inh.txt": {"Runner Initialization Params":
                                                {"l_label_col": 11,
                                                 "label_func": functools.partial(replace_filter_by_label,
                                                                                 *["INH", "None", False])}
                                            },
                    "sensitivity_pza.txt": {"Runner Initialization Params":
                                                {"l_label_col": 11,
                                                 "label_func": functools.partial(replace_filter_by_label,
                                                                                 *["PZA", "None", False])}
                                            },
                    "sensitivity_emb.txt": {"Runner Initialization Params":
                                                {"l_label_col": 11,
                                                 "label_func": functools.partial(replace_filter_by_label,
                                                                                 *["EMB", "None", False])}
                                            },
                    "sensitivity_rif.txt": {"Runner Initialization Params":
                                                {"l_label_col": 11,
                                                 "label_func": functools.partial(replace_filter_by_label,
                                                                                 *["RIF", "None", False])}
                                            },
                    "sensitivity_mfx.txt": {"Runner Initialization Params":
                                                {"l_label_col": 11,
                                                 "label_func": functools.partial(replace_filter_by_label,
                                                                                 *["MFX", "None", False])}
                                            },
                    "sensitivity_unknown.txt": {"Runner Initialization Params":
                                                    {"l_label_col": 11,
                                                     "label_func": functools.partial(replace_filter_by_label,
                                                                                     *["Unknown", "None", False])}
                                                },
                    "sputum_conversion_2": {"Runner Initialization Params":
                                                {"ids_list": ids_list, "data_list": repeated_data_list,
                                                 "l_label_col": 12,
                                                 "label_func": functools.partial(replace_filter,
                                                                                 lambda label: label[0:4])},
                                            "Runtime Params": {"classify_func": sputum_classify}
                                            },
                    "tb_contact.txt": {"Runner Initialization Params": {"l_label_col": 5}},
                    "tb_old.txt": {"Runner Initialization Params": {"l_label_col": 6}},
                    "diag_ltbi.txt": {"Runner Initialization Params":
                                          {"l_label_col": 8,
                                           "label_func": functools.partial(replace_label_with_required,
                                                                           {"Active TB": "None"})}
                                      },
                    "inh_medication_2.txt": {"Runner Initialization Params":
                                                 {"l_label_col": [13, 14, 15, 16, 17],
                                                  "label_func": functools.partial(replace_labels_with_required,
                                                                                  *["Isoniazid (INH)", "None"])},
                                             "Runtime Params": {"label_func": None, "pwds": pwds}
                                             },
                    "pyrazinamide_medication.txt": {"Runner Initialization Params":
                                                        {"l_label_col": [13, 14, 15, 16, 17],
                                                         "label_func": functools.partial(replace_labels_with_required,
                                                                                         *["Pyrazinamide (Z/Pza)",
                                                                                           "None"])},
                                                    "Runtime Params": {"label_func": None, "pwds": pwds}
                                                    },
                    "rifampin_medication.txt": {"Runner Initialization Params":
                                                    {"l_label_col": [13, 14, 15, 16, 17],
                                                     "label_func": functools.partial(replace_labels_with_required,
                                                                                     *["Rifampin (RIF)", "None"])},
                                                "Runtime Params": {"label_func": None, "pwds": pwds}
                                                },
                    "ethambutol_medication.txt": {"Runner Initialization Params":
                                                      {"l_label_col": [13, 14, 15, 16, 17],
                                                       "label_func": functools.partial(replace_labels_with_required,
                                                                                       *["Ethambutol (E/Emb)", "None"])
                                                       },
                                                  "Runtime Params": {"label_func": None, "pwds": pwds}
                                                  },
                    "rifabutin_medication.txt": {"Runner Initialization Params":
                                                     {"l_label_col": [13, 14, 15, 16, 17],
                                                      "label_func": functools.partial(replace_labels_with_required,
                                                                                      *["Rifabutin (Rfb)", "None"])},
                                                 "Runtime Params": {"label_func": None, "pwds": pwds}
                                                 },
                    "moxifloxacin_medication.txt": {"Runner Initialization Params":
                                                        {"l_label_col": [13, 14, 15, 16, 17],
                                                         "label_func": functools.partial(replace_labels_with_required,
                                                                                         *["Moxifloxacin (Mfx)",
                                                                                           "None"])},
                                                    "Runtime Params": {"label_func": None, "pwds": pwds}
                                                    },
                    "rifapentine_medication.txt": {"Runner Initialization Params":
                                                       {"l_label_col": [13, 14, 15, 16, 17],
                                                        "label_func": functools.partial(replace_labels_with_required,
                                                                                        *["Rifapentine (RPT)",
                                                                                          "None"])},
                                                   "Runtime Params": {"label_func": None, "pwds": pwds}
                                                   },
                    "capreomycin_medication.txt": {"Runner Initialization Params":
                                                       {"l_label_col": [13, 14, 15, 16, 17],
                                                        "label_func": functools.partial(replace_labels_with_required,
                                                                                        *["Capreomycin (Cm)", "None"])},
                                                   "Runtime Params": {"label_func": None, "pwds": pwds}
                                                   },
                    "amikacin_medication.txt": {"Runner Initialization Params":
                                                    {"l_label_col": [13, 14, 15, 16, 17],
                                                     "label_func": functools.partial(replace_labels_with_required,
                                                                                     *["Amikacin (Amk)", "None"])},
                                                "Runtime Params": {"label_func": None, "pwds": pwds}
                                                },
                    "pas_medication.txt": {"Runner Initialization Params":
                                               {"l_label_col": [13, 14, 15, 16, 17],
                                                "label_func": functools.partial(replace_labels_with_required,
                                                                                *["Para-aminosalicylic acid (Pas)",
                                                                                  "None"])},
                                           "Runtime Params": {"label_func": None, "pwds": pwds}
                                           },
                    "cycloserine_medication.txt": {"Runner Initialization Params":
                                                       {"l_label_col": [13, 14, 15, 16, 17],
                                                        "label_func": functools.partial(replace_labels_with_required,
                                                                                        *["Cycloserine (Dcs)", "None"])
                                                        },
                                                   "Runtime Params": {"label_func": None, "pwds": pwds}
                                                   },
                    "ethionamide_medication.txt": {"Runner Initialization Params":
                                                       {"l_label_col": [13, 14, 15, 16, 17],
                                                        "label_func": functools.partial(replace_labels_with_required,
                                                                                        *["Ethionamide (Eto)", "None"])
                                                        },
                                                   "Runtime Params": {"label_func": None, "pwds": pwds}
                                                   },
                    "vitamin_b6_medication.txt": {"Runner Initialization Params":
                                                      {"l_label_col": [13, 14, 15, 16, 17],
                                                       "label_func": functools.partial(replace_labels_with_required,
                                                                                       *["Vitamin B6", "None"])},
                                                  "Runtime Params": {"label_func": None, "pwds": pwds}
                                                  },
                    "hcw": {"Runner Initialization Params":
                                {"l_id_col": 0, "l_label_col": 1, "label_file": label_filename2},
                            "Runtime Params": {"label_func": None, "pwds": pwds}},
                    "corticosteroids_immuno.txt": {"Runner Initialization Params":
                                                       {"l_label_col": 26,
                                                        "label_func": functools.partial(replace_label_with_required,
                                                                                        {
                                                                                            "Corticosteroids (prednisone)": "Yes",
                                                                                            "Other": "No", 'None': "No",
                                                                                            "Chemotherapy": "No",
                                                                                            "TNF alpha inhibitors": "No"})},

                                                   "Runtime Params": {
                                                       "preprocess_func": immuno_preprocessor.preprocess}},
                    "chemotherapy_immuno": {"Runner Initialization Params":
                                                {"l_label_col": 21,
                                                 "label_func": functools.partial(replace_label_with_required,
                                                                                 {"Corticosteroids (prednisone)": "No",
                                                                                  "Other": "No", 'None': "No",
                                                                                  "Chemotherapy": "Yes",
                                                                                  "TNF alpha inhibitors": "No"})}
                                            },
                    "TNF_immuno": {"Runner Initialization Params":
                                       {"l_label_col": 21,
                                        "label_func": functools.partial(replace_label_with_required,
                                                                        {"Corticosteroids (prednisone)": "No",
                                                                         "Other": "No", 'None': "No",
                                                                         "Chemotherapy": "No",
                                                                         "TNF alpha inhibitors": "Yes"})},
                                   },
                    "BCG": {"Runner Initialization Params": {"l_id_col": 0, "l_label_col": 7,
                                                             "label_file": label_filename2}},
                    "smh": {"Runner Initialization Params": {"l_id_col": 0, "l_label_col": 3,
                                                             "label_file": label_filename2, "l_first_row": 1}},
                    "afb_positive.txt": {"Runner Initialization Params": {"l_label_col": 25,
                                                                          "label_file": label_filename3,
                                                                          "label_func": functools.partial(
                                                                              replace_labels_with_required,
                                                                              "Pulmonary AFB Positive", "None")}},
                    "disseminated.txt": {"Runner Initialization Params": {"l_label_col": 35,
                                                                          "label_func": functools.partial(
                                                                              replace_labels_with_required,
                                                                              "Disseminated", "None")}},
                    "extra_pulmonary.txt": {"Runner Initialization Params": {"l_label_col": 25,
                                                                             "label_file": label_filename3,
                                                                             "label_func": functools.partial(
                                                                                 replace_labels_with_required,
                                                                                 "Extra Pulmonary (localized)",
                                                                                 "None")}},
                    "other_tb_risk_factors": {"Runner Initialization Params": {"l_label_col": 23}},
                    "tb_duration": {"use_row_start": True, "Runner Initialization Params": {"l_label_col": 40,
                                                                                            "ids_list": ids_list,
                                                                                            "data_list": repeated_data_list},
                                    },

                    "skin_test_mm.txt": {"Runner Initialization Params": {"l_id_col": 0, "l_label_col": 5,
                                                                          "label_file": label_filename2,
                                                                          "l_first_row": 1,
                                                                          },
                                         "Runtime Params": {"classify_func": max_classify}
                                         },
                    "skin_test": {"Runner Initialization Params": {"l_id_col": 0, "l_label_col": 9,
                                                                   "label_file": label_filename2, "l_first_row": 1,
                                                                   },
                                  "Runtime Params": {"label_func": None, "pwds": pwds}
                                  },
                    "treatment_interruption.txt": {"use_row_start": True,
                                                   "Runner Initialization Params": {"l_label_col": 42,
                                                                                    "label_func": functools.partial(
                                                                                        replace_label_with_required,
                                                                                        {"1": "Yes",
                                                                                         "0": "No"}
                                                                                    )}},
                    "sputum_conversion.txt": {"Runner Initialization Params": {"ids_list": ids_list,
                                                                               "label_file": label_filename3,
                                                                               "l_label_col": 12,
                                                                               "label_func": functools.partial(
                                                                                   replace_filter,
                                                                                   lambda label: label[0:4])}
                                              }
                    }

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
    for each in file_to_args:
        if each == variable or each == variable + ".txt":
            variable = each
            break
    cur_run = [variable]
    # cur_run = ["inh_medication_2.txt"]

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
            ids["all"], data["all"], labels["all"] = di.get_labeled_data(**cur_params)
            classifier_runner = load_classifier_data(classifier_runner, data["all"], labels['all'], ids["all"],
                                                     create_train_valid=True, train_percent=.6, random_seed=0)
        else:
            for cur_dataset in datasets:
                if "use_row_start" in file_to_args[rule]:
                    cur_params['l_first_row'] = row_start[cur_dataset]
                cur_params["label_file"] = label_files_dict[cur_dataset]
                ids[cur_dataset], data[cur_dataset], labels[cur_dataset]  = di.get_labeled_data(**cur_params)
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
            classifier_classes = sorted(list(classifier_runner.classifier_parameters["regexes"]))

            if classifier_type == "CaptureClassifier":
                cnf_matrix = None


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