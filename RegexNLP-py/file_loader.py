import os
from datahandler import data_import as di
from datahandler.preprocessors import *

filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'CombinedData.csv')
label_filename2 = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Dev Labelling Decisions',
                               'labelling_decisions_cohort_2-s.xlsx')

label_filename3 = os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx')

label_files_dict = dict()
label_files_dict["train"] = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Train_set_labels.xlsx')
label_files_dict["valid"] = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Valid_set_labels.xlsx')
# test_label_filename = os.path.join(os.getenv('TB_DATA_FOLDER'), 'Test_set_labels.xlsx')

data_loader = di.data_from_csv if filename.endswith('.csv') else di.data_from_excel
data_list, _, ids_list = data_loader([filename], data_cols=2, first_row=1, id_cols=0, repeat_ids=False)
data_repeated, _, ids_repeated = data_loader([filename], data_cols=2, first_row=1, id_cols=0, repeat_ids=True)

_, repeated_data_list, repeated_labels_list = convert_repeated_data_to_sublist(ids_repeated,
                                                                               repeated_data=data_repeated)
