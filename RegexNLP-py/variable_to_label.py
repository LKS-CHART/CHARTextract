import csv
# variable_to_label_file = {
#     "hiv_positive": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "HIV Positive"
#     },
#
#     "hiv_negative": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "HIV Negative"
#     },
#
#     "hiv_unknown": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "HIV Unknown"
#     },
#
#     "hiv_not_dictated": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "HIV Not dictated"
#     },
#
#     "tb_contact": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "TB Contact (Yes or No) #Note: Rules for >= 2 years or <= 2 years in phase 2"
#     },
#
#     "tb_old": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "Old TB"
#     },
#
#     "tb_old_not_dictated": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "Old TB - Not Dictated"
#     },
#
#     "disseminated": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "Extent of Active TB - Disseminated"
#     },
#
#     "afb_positive": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "Pulmonary AFB Positive"
#     },
#
#     "extra_pulmonary": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "Extra Pulmonary"
#     },
#
#     "diag_active": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "Active TB"
#     },
#
#     "diag_ltbi": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "LTBI"
#     },
#
#     "diag_ntm": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "NTM"
#     },
#
#     "diag_method_culture": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "Method of Diagnosis (Culture Positive)"
#     }
#     ,
#     "diag_method_pcr": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 2,
#         "Variable Name": "Method of Diagnosis (PCR Positive)"
#     },
#     "corticosteroids_immuno": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/immunosuppressive_labels.csv",
#         "Label Id Col": 0,
#         "Label First Row": 1,
#         "Variable Name": "On Immunosuppressive Medication (Corticosteroids)"
#     },
#     "chemotherapy_immuno": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/immunosuppressive_labels.csv",
#         "Label Id Col": 0,
#         "Label First Row": 1,
#         "Variable Name": "On Immunosuppressive Medication (Chemotherapy)"
#     },
#     "other_immuno": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/immunosuppressive_labels.csv",
#         "Label Id Col": 0,
#         "Label First Row": 1,
#         "Variable Name": "On Immunosuppressive Medication (Other)"
#     },
#     "ad_rx_reaction_gi": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "Adverse Drug Reactions (GI)"
#     },
#     "ad_rx_peripheral_neuropathy": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "Adverse Drug Reactions (Peripheral Neuropathy)"
#     },
#     "ad_rx_rash": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "Adverse Drug Reactions (Rash)"
#     },
#     "ad_rx_ocular_toxicity": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "Adverse Drug Reactions (Ocular Toxicity)"
#     },
#     "sensitivity_inh": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "INH Sensitive"
#     },
#     "sensitivity_pza": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "PZA Sensitive"
#     },
#     "sensitivity_full": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "Fully Sensitive"
#     },
#     "sensitivity_unknown": {
#         "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Train_set_labels.xlsx",
#         "Valid Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Valid_set_labels.xlsx",
#         "Label Id Col": 1,
#         "Label First Row": 3,
#         "Variable Name": "Sensitivities Unknown"
#     }
# }

variable_to_label_file = {
    "hiv_positive": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "HIV Positive"
    },

    "hiv_negative": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "HIV Negative"
    },

    "hiv_unknown": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "HIV Unknown"
    },

    "hiv_not_dictated": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "HIV Not dictated"
    },

    "tb_contact": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "TB Contact (Yes or No) #Note: Rules for >= 2 years or <= 2 years in phase 2"
    },

    "tb_old": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "Old TB"
    },

    "tb_old_not_dictated": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "Old TB - Not Dictated"
    },

    "disseminated": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "Extent of Active TB - Disseminated"
    },

    "afb_positive": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "Pulmonary AFB Positive"
    },

    "extra_pulmonary": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "Extra Pulmonary"
    },

    "diag_active": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "Active TB"
    },

    "diag_ltbi": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "LTBI"
    },

    "diag_ntm": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "NTM"
    },

    "diag_method_culture": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "Method of Diagnosis (Culture Positive)"
    }
    ,
    "diag_method_pcr": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Manual Chart Extraction - Cohort 3.xlsx",
        "Label Id Col": 1,
        "Label First Row": 2,
        "Variable Name": "Method of Diagnosis (PCR Positive)"
    },
    "corticosteroids_immuno": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/immunosuppressive_labels_test.csv",
        "Label Id Col": 0,
        "Label First Row": 1,
        "Variable Name": "On Immunosuppressive Medication (Corticosteroids)"
    },
    "chemotherapy_immuno": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/immunosuppressive_labels_test.csv",
        "Label Id Col": 0,
        "Label First Row": 1,
        "Variable Name": "On Immunosuppressive Medication (Chemotherapy)"
    },
    "other_immuno": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/immunosuppressive_labels_test.csv",
        "Label Id Col": 0,
        "Label First Row": 1,
        "Variable Name": "On Immunosuppressive Medication (Other)"
    },
    "ad_rx_reaction_gi": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "Adverse Drug Reactions (GI)"
    },
    "ad_rx_peripheral_neuropathy": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "Adverse Drug Reactions (Peripheral Neuropathy)"
    },
    "ad_rx_rash": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "Adverse Drug Reactions (Rash)"
    },
    "ad_rx_ocular_toxicity": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "Adverse Drug Reactions (Ocular Toxicity)"
    },
    "sensitivity_inh": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "INH Sensitive"
    },
    "sensitivity_pza": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "PZA Sensitive"
    },
    "sensitivity_full": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "Fully Sensitive"
    },
    "sensitivity_unknown": {
        "Label File": "Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/Test_set_labels.xlsx",
        "Label Id Col": 1,
        "Label First Row": 3,
        "Variable Name": "Sensitivities Unknown"
    }
}

tool_errors = set()
with open("tool_errors.txt") as f:
    lines = csv.reader(f, delimiter=',', quotechar='"')
    for i, line in enumerate(lines):
        for token in line:
            patient, variable = token.split("-")
            patient = patient.strip()
            variable = variable.strip()
            tool_errors.add((patient,variable))

print(tool_errors)