import re
import openpyxl
import csv

def get_data():
    pass

def data_from_excel(filenames, data_cols=None, label_cols=None, id_cols=None, repeat_ids=True, first_row=1, limit=None):
    '''
    Reads data from the filenames

    :param filenames: List of Excel filenames (List of strings)
    :param data_cols: List of location of data columns in each file  (List of int)
    :param label_cols: List of location of label columns in each file  (List of int)
    :param id_cols: List of location of id columns in each file  (List of int)
    :param repeat_ids: If True, data corresponding to already existing ids are concatenated (Boolean)
    :param first_row: Starts reading from specified row number (int)
    :param limit: Stops reading after specified number of lines have been read (int)

    :return: list of data, list of labels, list of ids
    '''

    data = None
    labels = None
    ids = None

    print("Reading data from excel file")

    count = 0
    for file_num, filename in enumerate(filenames):
        workbook = openpyxl.load_workbook(filename, data_only=True, read_only=False)
        sheet_names = workbook.get_sheet_names()
        for sheet_name in sheet_names:
            #getting rows in worksheet
            cur_ws = workbook[sheet_name].rows
            for i, row in enumerate(cur_ws):
                if i >= first_row:
                    count += 1
                    data, labels, ids = get_data()


    return data, labels, ids


