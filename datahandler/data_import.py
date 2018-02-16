import re
import openpyxl
import csv

def get_data(row, data_cols, label_cols, id_cols, data, labels, ids, repeat_ids):
    pass

def _data_helper(num_files, data_cols=None, label_cols=None, id_cols=None):
    '''
    Initializes data, labels and ids and data_cols, label_cols, id_cols as a list

    :param num_files:  number of files
    :param data_cols: location of data (int or list of int)
    :param label_cols: location of labels (int or list of ints)
    :param id_cols: location of ids (int or list of ints)

    :return: data, labels, ids, data_cols, label_cols, id_cols
    '''
    data = None
    labels = None
    ids = None

    if data_cols is not None:
        if type(data_cols) == int:
            data_cols = [data_cols]*num_files
        data = []

    if label_cols is not None:
        if type(label_cols) == int:
            label_cols = [label_cols]*num_files
        labels = []

    if id_cols is not None:
        if type(id_cols) == int:
            id_cols = [id_cols]*num_files
        ids = []

    return data, labels, ids, data_cols, label_cols, id_cols


def data_from_excel(filenames, data_cols=None, label_cols=None, id_cols=None, repeat_ids=True, first_row=1, limit=None):
    '''
    Reads data from the filenames

    :param filenames: List of Excel filenames (List of strings)
    :param data_cols: List of location of data columns in each file  (List of int or int)
    :param label_cols: List of location of label columns in each file  (List of int or int)
    :param id_cols: List of location of id columns in each file  (List of int or int)
    :param repeat_ids: If True, data corresponding to already existing ids are concatenated (Boolean)
    :param first_row: Starts reading from specified row number (int)
    :param limit: Stops reading after specified number of lines have been read (int)

    :return: list of data, list of labels, list of ids
    '''

    data, labels, ids, data_cols, label_cols, id_cols = _data_helper(len(filenames), data_cols, label_cols, id_cols)

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
                    data, labels, ids = get_data(row, data_cols[file_num], label_cols[file_num], id_cols[file_num],
                                                 data, labels, ids, repeat_ids)


    return data, labels, ids


