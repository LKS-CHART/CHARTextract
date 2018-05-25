from util.tb_country import preprocess
import functools
from classifier.classification_functions import *
from file_loader import *
from util.pwd_preprocessors import *
from datahandler import data_import as di

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

label_filename3 = os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx')

label_files_dict = dict()
label_files_dict["train"] = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Train_set_labels.xlsx')
label_files_dict["valid"] = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Valid_set_labels.xlsx')
# test_label_filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Test_set_labels.xlsx')

rules_path = os.path.join(os.getenv('TB_DATA_FOLDER'), 'rules')
dummy_rules_path = os.path.join(*["examples", "regexes", "tb_regexes"])

tb_rules = os.path.join(rules_path, "tb_rules")


file_to_args = {"smoking_new": {"Runner Initialization Params": {"l_label_col": 7}},
                "country": {"Runner Initialization Params": {"l_label_col": 2}, "Runtime Params":
                    {"label_func": None, "preprocess_func": preprocess}},
                "diagnosis": {"Runner Initialization Params": {"l_label_col": 8}},
                "diag_active": {"Runner Initialization Params":
                                        {"l_label_col": 8,
                                         "label_func": functools.partial(replace_label_with_required,
                                                                         {"LTBI": "None"})},
                                    "Runtime Params": {"pwds": pwds}
                                    },
                "diag_method_clinical": {"Runner Initialization Params":
                                                 {"l_label_col": 10,
                                                  "label_func": functools.partial(replace_label_with_required,
                                                                                  {"PCR positive": "None",
                                                                                   "Culture positive": "None"})}
                                             },
                "diag_method_culture": {"Runner Initialization Params":
                                                {"l_label_col": 10,
                                                 "label_func": functools.partial(replace_label_with_required,
                                                                                 {"PCR positive": "None",
                                                                                  "Clinical diagnosis": "None"})}
                                            },
                "diag_method_pcr": {"Runner Initialization Params":
                                            {"l_label_col": 10,
                                             "label_func": functools.partial(replace_label_with_required,
                                                                             {"Clinical diagnosis": "None",
                                                                              "Culture positive": "None"})}
                                        },
                "diag_ntm": {"Runner Initialization Params": {"l_label_col": 9}},
                "hiv_negative": {"Runner Initialization Params":
                                         {"l_label_col": 4,
                                          "label_func": functools.partial(replace_label_with_required,
                                                                          {"Positive": "None", "Unknown": "None"})}
                                     },
                "hiv_positive": {"Runner Initialization Params":
                                         {"l_label_col": 4,
                                          "label_func": functools.partial(replace_label_with_required,
                                                                          {"Negative": "None", "Unknown": "None"})}
                                     },
                "hiv_not_dictated": {"Runner Initialization Params":
                                             {"l_label_col": 4,
                                              "label_func": functools.partial(replace_label_with_required,
                                                                              {"Positive": "None",
                                                                               "Unknown": "None",
                                                                               "Negative": "None",
                                                                               "None": "Not dictated"})}
                                         },
                "hiv_unknown": {"Runner Initialization Params":
                                        {"l_label_col": 4,
                                         "label_func": functools.partial(replace_label_with_required,
                                                                         {"Positive": "None", "Negative": "None"})}
                                    },
                "immigration": {"Runner Initialization Params":
                                        {"l_label_col": 3,
                                         "label_func":  functools.partial(replace_filter, lambda label: label[0:4]),
                                         "label_file": label_filename3}
                                    },
                "sensitivity_full": {"Runner Initialization Params":
                                             {"l_label_col": 11,
                                              "label_func": functools.partial(replace_labels_with_required,
                                                                              *["Fully Sensitive", "None"])},
                                         },
                "sensitivity_inh": {"Runner Initialization Params":
                                            {"l_label_col": 11,
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["INH", "None", False])}
                                        },
                "sensitivity_pza": {"Runner Initialization Params":
                                            {"l_label_col": 11,
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["PZA", "None", False])}
                                        },
                "sensitivity_emb": {"Runner Initialization Params":
                                            {"l_label_col": 11,
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["EMB", "None", False])}
                                        },
                "sensitivity_rif": {"Runner Initialization Params":
                                            {"l_label_col": 11,
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["RIF", "None", False])}
                                        },
                "sensitivity_mfx": {"Runner Initialization Params":
                                            {"l_label_col": 11,
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["MFX", "None", False])}
                                        },
                "sensitivity_unknown": {"Runner Initialization Params":
                                                {"l_label_col": 11,
                                                 "label_func": functools.partial(replace_filter_by_label,
                                                                                 *["Unknown", "None", False])}
                                            },
                "sputum_conversion_2": {"Runner Initialization Params":
                                            {"ids_list": ids_list, "data_list": repeated_data_list,
                                             "l_label_col": 12,
                                             "label_func": functools.partial(replace_filter, lambda label: label[0:4])},
                                        "Runtime Params": {"classify_func": sputum_classify}
                                        },
                "tb_contact": {"Runner Initialization Params": {"l_label_col": 5}},
                "tb_old": {"Runner Initialization Params": {"l_label_col": 6}},
                "diag_ltbi": {"Runner Initialization Params":
                                      {"l_label_col": 8,
                                       "label_func": functools.partial(replace_label_with_required,
                                                                       {"Active TB": "None"})}
                                  },
                "inh_medication_2": {"Runner Initialization Params":
                                             {"l_label_col": [13, 14, 15, 16, 17],
                                              "label_func": functools.partial(replace_labels_with_required, *["Isoniazid (INH)", "None"])},
                                         "Runtime Params": {"label_func": None, "pwds": pwds}
                                         },
                "pyrazinamide_medication": {"Runner Initialization Params":
                                                    {"l_label_col": [13, 14, 15, 16, 17],
                                                     "label_func": functools.partial(replace_labels_with_required,
                                                                                     *["Pyrazinamide (Z/Pza)",
                                                                                       "None"])},
                                                "Runtime Params": {"label_func": None, "pwds": pwds}
                                                },
                "rifampin_medication": {"Runner Initialization Params":
                                                {"l_label_col": [13, 14, 15, 16, 17],
                                                 "label_func": functools.partial(replace_labels_with_required,
                                                                                 *["Rifampin (RIF)", "None"])},
                                            "Runtime Params": {"label_func": None, "pwds": pwds}
                                            },
                "ethambutol_medication": {"Runner Initialization Params":
                                                  {"l_label_col": [13, 14, 15, 16, 17],
                                                   "label_func": functools.partial(replace_labels_with_required,
                                                                                   *["Ethambutol (E/Emb)", "None"])
                                                   },
                                              "Runtime Params": {"label_func": None, "pwds": pwds}
                                              },
                "rifabutin_medication": {"Runner Initialization Params":
                                                 {"l_label_col": [13, 14, 15, 16, 17],
                                                  "label_func": functools.partial(replace_labels_with_required,
                                                                                  *["Rifabutin (Rfb)", "None"])},
                                             "Runtime Params": {"label_func": None, "pwds": pwds}
                                             },
                "moxifloxacin_medication": {"Runner Initialization Params":
                                                    {"l_label_col": [13, 14, 15, 16, 17],
                                                     "label_func": functools.partial(replace_labels_with_required,
                                                                                     *["Moxifloxacin (Mfx)",
                                                                                       "None"])},
                                                "Runtime Params": {"label_func": None, "pwds": pwds}
                                                },
                "rifapentine_medication": {"Runner Initialization Params":
                                                   {"l_label_col": [13, 14, 15, 16, 17],
                                                    "label_func": functools.partial(replace_labels_with_required,
                                                                                    *["Rifapentine (RPT)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}
                                               },
                "capreomycin_medication": {"Runner Initialization Params":
                                                   {"l_label_col": [13, 14, 15, 16, 17],
                                                    "label_func": functools.partial(replace_labels_with_required,
                                                                                    *["Capreomycin (Cm)", "None"])},
                                               "Runtime Params": {"label_func": None, "pwds": pwds}
                                               },
                "amikacin_medication": {"Runner Initialization Params":
                                                {"l_label_col": [13, 14, 15, 16, 17],
                                                 "label_func": functools.partial(replace_labels_with_required,
                                                                                 *["Amikacin (Amk)", "None"])},
                                            "Runtime Params": {"label_func": None, "pwds": pwds}
                                            },
                "pas_medication": {"Runner Initialization Params":
                                           {"l_label_col": [13, 14, 15, 16, 17],
                                            "label_func": functools.partial(replace_labels_with_required,
                                                                            *["Para-aminosalicylic acid (Pas)",
                                                                              "None"])},
                                       "Runtime Params": {"label_func": None, "pwds": pwds}
                                       },
                "cycloserine_medication": {"Runner Initialization Params":
                                                   {"l_label_col": [13, 14, 15, 16, 17],
                                                    "label_func": functools.partial(replace_labels_with_required,
                                                                                    *["Cycloserine (Dcs)", "None"])
                                                    },
                                               "Runtime Params": {"label_func": None, "pwds": pwds}
                                               },
                "ethionamide_medication": {"Runner Initialization Params":
                                                   {"l_label_col": [13, 14, 15, 16, 17],
                                                    "label_func": functools.partial(replace_labels_with_required,
                                                                                    *["Ethionamide (Eto)", "None"])
                                                    },
                                               "Runtime Params": {"label_func": None, "pwds": pwds}
                                               },
                "vitamin_b6_medication": {"Runner Initialization Params":
                                                  {"l_label_col": [13, 14, 15, 16, 17],
                                                   "label_func": functools.partial(replace_labels_with_required,
                                                                                   *["Vitamin B6", "None"])},
                                              "Runtime Params": {"label_func": None, "pwds": pwds}
                                              },
                "hcw": {"Runner Initialization Params":
                            {"l_id_col": 0, "l_label_col": 1, "label_file": label_filename2},
                        "Runtime Params": {"label_func": None, "pwds": pwds}},
                "corticosteroids_immuno": {"Runner Initialization Params":
                                                   {"l_label_col": 26,
                                                    "label_func": functools.partial(replace_label_with_required,
                                                                                    {"Corticosteroids (prednisone)": "Yes",
                                                                                     "Other": "No", 'None': "No",
                                                                                     "Chemotherapy": "No",
                                                                                     "TNF alpha inhibitors": "No"})},

                                               "Runtime Params": {"preprocess_func": immuno_preprocessor.preprocess}},
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
                "afb_positive": {"Runner Initialization Params": {"l_label_col": 25,
                                                                      "label_file": label_filename3,
                                                                      "label_func": functools.partial(replace_labels_with_required,
                                                                                                      "Pulmonary AFB Positive", "None")}},
                "disseminated": {"Runner Initialization Params": {"l_label_col": 35,
                                                                      "label_func": functools.partial(replace_labels_with_required,
                                                                                                      "Disseminated", "None")}},
                "extra_pulmonary": {"Runner Initialization Params": {"l_label_col": 25,
                                                                         "label_file": label_filename3,
                                                                         "label_func": functools.partial(replace_labels_with_required,
                                                                                                         "Extra Pulmonary (localized)", "None")}},
                "other_tb_risk_factors": {"Runner Initialization Params": {"l_label_col": 23}},
                "tb_duration": {"use_row_start": True, "Runner Initialization Params": {"l_label_col": 40,
                                                                                        "ids_list": ids_list,
                                                                                        "data_list": repeated_data_list},
                                },

                "skin_test_mm": {"Runner Initialization Params": {"l_id_col": 0, "l_label_col": 5,
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
                "treatment_interruption": {"use_row_start": True, "Runner Initialization Params": {"l_label_col": 42,
                                                                                                       "label_func": functools.partial(
                                                                                                           replace_label_with_required,
                                                                                                           {"1": "Yes",
                                                                                                            "0": "No"}
                                                                                                       )}},
                "sputum_conversion": {"Runner Initialization Params": {"ids_list": ids_list,
                                                                           "label_file": label_filename3,
                                                                           "l_label_col": 12,
                                                                           "label_func": functools.partial(replace_filter, lambda label: label[0:4])}
                                          }
                }
