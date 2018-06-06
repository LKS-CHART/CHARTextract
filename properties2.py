from util.tb_country import preprocess
import functools
from classifier.classification_functions import *
from datahandler.preprocessors import *

file_to_args = {
                "homelessness": {"Runner Initialization Params": {"label_func": functools.partial(
                    replace_labels_with_required, *["Homeless shelter", "None"])}},
                "country": {"Runtime Params": {"preprocess_func": preprocess}},
                "diag_active": {"Runner Initialization Params":
                                    {"label_func": functools.partial(replace_label_with_required,
                                                                     {"LTBI": "None"})
                                    }
                                },
                "diag_method_clinical": {"Runner Initialization Params":
                                                 {
                                                  "label_func": functools.partial(replace_label_with_required,
                                                                                  {"PCR positive": "None",
                                                                                   "Culture positive": "None"})
                                                 }
                                         },
                "diag_method_culture": {"Runner Initialization Params":
                                                {
                                                 "label_func": functools.partial(replace_label_with_required,
                                                                                 {"PCR positive": "None",
                                                                                  "Clinical diagnosis": "None"})
                                                }
                                        },
                "diag_method_pcr": {"Runner Initialization Params":
                                            {
                                             "label_func": functools.partial(replace_label_with_required,
                                                                             {"Clinical diagnosis": "None",
                                                                              "Culture positive": "None"})}
                                        },
                "hiv_negative": {"Runner Initialization Params":
                                         {
                                          "label_func": functools.partial(replace_label_with_required,
                                                                          {"Positive": "None", "Unknown": "None"})}
                                     },
                "hiv_positive": {"Runner Initialization Params":
                                         {
                                          "label_func": functools.partial(replace_label_with_required,
                                                                          {"Negative": "None", "Unknown": "None"})}
                                     },
                "hiv_not_dictated": {"Runner Initialization Params":
                                             {
                                              "label_func": functools.partial(replace_label_with_required,
                                                                              {"Positive": "None",
                                                                               "Unknown": "None",
                                                                               "Negative": "None",
                                                                               "None": "Not dictated"})}
                                         },
                "hiv_unknown": {"Runner Initialization Params":
                                        {
                                         "label_func": functools.partial(replace_label_with_required,
                                                                         {"Positive": "None", "Negative": "None"})}
                                    },
                "immigration": {"Runner Initialization Params":
                                        {
                                         "label_func":  functools.partial(replace_filter, lambda label: label[0:4]),
                                    }},
                "sensitivity_full": {"Runner Initialization Params":
                                             {
                                              "label_func": functools.partial(replace_labels_with_required,
                                                                              *["Fully Sensitive", "None"])},
                                         },
                "sensitivity_inh": {"Runner Initialization Params":
                                            {
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["INH", "None", False])}
                                        },
                "sensitivity_pza": {"Runner Initialization Params":
                                            {
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["PZA", "None", False])}
                                        },
                "sensitivity_emb": {"Runner Initialization Params":
                                            {
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["EMB", "None", False])}
                                        },
                "sensitivity_rif": {"Runner Initialization Params":
                                            {
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["RIF", "None", False])}
                                        },
                "sensitivity_mfx": {"Runner Initialization Params":
                                            {
                                             "label_func": functools.partial(replace_filter_by_label,
                                                                             *["MFX", "None", False])}
                                        },
                "sensitivity_unknown": {"Runner Initialization Params":
                                                {
                                                 "label_func": functools.partial(replace_filter_by_label,
                                                                                 *["Unknown", "None", False])}
                                            },
                "diag_ltbi": {"Runner Initialization Params":
                                      {
                                       "label_func": functools.partial(replace_label_with_required,
                                                                       {"Active TB": "None"})}
                                  },
                "inh_medication": {"Runner Initialization Params":
                                             {
                                              "label_func": functools.partial(replace_labels_with_required, *["Isoniazid (INH)", "None"])},
                                         },
                "pyrazinamide_medication": {"Runner Initialization Params":
                                                    {
                                                     "label_func": functools.partial(replace_labels_with_required,
                                                                                     *["Pyrazinamide (Z/Pza)",
                                                                                       "None"])},
                                                },
                "rifampin_medication": {"Runner Initialization Params":
                                                {
                                                 "label_func": functools.partial(replace_labels_with_required,
                                                                                 *["Rifampin (RIF)", "None"])},
                                            },
                "ethambutol_medication": {"Runner Initialization Params":
                                                  {
                                                   "label_func": functools.partial(replace_labels_with_required,
                                                                                   *["Ethambutol (E/Emb)", "None"])
                                                   },
                                              },
                "rifabutin_medication": {"Runner Initialization Params":
                                                 {
                                                  "label_func": functools.partial(replace_labels_with_required,
                                                                                  *["Rifabutin (Rfb)", "None"])},
                                             },
                "moxifloxacin_medication": {"Runner Initialization Params":
                                                    {
                                                     "label_func": functools.partial(replace_labels_with_required,
                                                                                     *["Moxifloxacin (MFX)",
                                                                                       "None"])},
                                                },
                "rifapentine_medication": {"Runner Initialization Params":
                                                   {
                                                    "label_func": functools.partial(replace_labels_with_required,
                                                                                    *["Rifapentine (RPT)", "None"])},
                                               },
                "capreomycin_medication": {"Runner Initialization Params":
                                                   {
                                                    "label_func": functools.partial(replace_labels_with_required,
                                                                                    *["Capreomycin (Cm)", "None"])},
                                               },
                "amikacin_medication": {"Runner Initialization Params":
                                                {
                                                 "label_func": functools.partial(replace_labels_with_required,
                                                                                 *["Amikacin (Amk)", "None"])},
                                            },
                "pas_medication": {"Runner Initialization Params":
                                           {
                                            "label_func": functools.partial(replace_labels_with_required,
                                                                            *["Para-aminosalicylic acid (Pas)",
                                                                              "None"])},
                                       },
                "cycloserine_medication": {"Runner Initialization Params":
                                                   {
                                                    "label_func": functools.partial(replace_labels_with_required,
                                                                                    *["Cycloserine (Dcs)", "None"])
                                                    },
                                               },
                "ethionamide_medication": {"Runner Initialization Params":
                                                   {
                                                    "label_func": functools.partial(replace_labels_with_required,
                                                                                    *["Ethionamide (Eto)", "None"])
                                                    },
                                               },
                "vitamin_b6_medication": {"Runner Initialization Params":
                                                  {
                                                   "label_func": functools.partial(replace_labels_with_required,
                                                                                   *["Vitamin B6", "None"])},
                                              },
                "corticosteroids_immuno": {"Runner Initialization Params":
                                                   {
                                                    "label_func": functools.partial(replace_label_with_required,
                                                                                    {"Corticosteroids (prednisone)": "Yes",
                                                                                     "Other": "No", 'None': "No",
                                                                                     "Chemotherapy": "No",
                                                                                     "TNF alpha inhibitors": "No"})
                                                   }
                                           },
                "chemotherapy_immuno": {"Runner Initialization Params":
                                            {
                                             "label_func": functools.partial(replace_label_with_required,
                                                                             {"Corticosteroids (prednisone)": "No",
                                                                              "Other": "No", 'None': "No",
                                                                              "Chemotherapy": "Yes",
                                                                              "TNF alpha inhibitors": "No"})}
                                        },
                "TNF_immuno": {"Runner Initialization Params":
                                   {
                                    "label_func": functools.partial(replace_label_with_required,
                                                                    {"Corticosteroids (prednisone)": "No",
                                                                     "Other": "No", 'None': "No",
                                                                     "Chemotherapy": "No",
                                                                     "TNF alpha inhibitors": "Yes"})},
                               },
                "afb_positive": {"Runner Initialization Params": {"label_func": functools.partial(
                                                                    replace_labels_with_required,
                                                                    "Pulmonary AFB Positive", "None")}},
                "disseminated": {"Runner Initialization Params": {"label_func": functools.partial(
                                                                    replace_labels_with_required,
                                                                    "Disseminated", "None")}},
                "extra_pulmonary": {"Runner Initialization Params": {"label_func": functools.partial(
                                                                        replace_labels_with_required,
                                    "Extra Pulmonary (localized)", "None")}},

                "skin_test_mm": {"Runtime Params": {"classify_func": max_classify}},

                "treatment_interruption": {"Runner Initialization Params": {"label_func": functools.partial(
                                                                                replace_label_with_required,
                                                                                                        {"1": "Yes",
                                                                                                            "0": "No"}
                                                                                                       )}},
                "sputum_conversion": {"Runner Initialization Params": {"l_label_col": 12,
                                                                       "label_func": functools.partial(replace_filter,
                                                                                                       lambda label:
                                                                                                       label[0:4])
                                      }}}
