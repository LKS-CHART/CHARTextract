import re
import openpyxl
import csv

def preprocess_data(data):
    '''
    Preprocesses datta

    :param data: data (string)

    :return: modified data
    '''

    data = data.replace('_x000D_', '').replace('\n#\n', '\n').replace('#', '\n').replace('\\n','\n').lower()
    data, num_subs = re.subn(r'\s{3,}', " ", data)
    return data

def get_data(data_col, label_col, id_col, data, labels, ids, repeat_ids, row_process_func):
    '''
    Gets data, label and id from a row

    :param data_col: data column number (int)
    :param label_col: label column number (int)
    :param id_col: id column number (int)
    :param data: list of data so far (list)
    :param labels: list of labels so far (list)
    :param ids: list of ids so far (ids)
    :param repeat_ids: should repeated ids be allowed (bool)
    :param row_process_func: function that extracts a value from a row

    :return: modified data, labels, ids arrays
    '''
    concat_index = None

    if id_col is not None:
        cur_id = row_process_func(id_col)

        #if repeat ids is false and id in ids, we want to only use the latest record
        if not repeat_ids and cur_id in ids:
            concat_index = ids.index(cur_id)
        else:
            ids.append(cur_id)

        if label_col is not None:
            #If we are concatenating data (i.e repeat_ids = False), use the latest diagnoses
            if concat_index is not None:
                labels[concat_index] = row_process_func(label_col)
            else:
                labels.append(row_process_func(label_col))

        if data_col is not None:
            datum = row_process_func(data_col)
            if concat_index is not None:
                data[concat_index] += "{}\n".format(datum)
            else:
                data.append(datum)


    return data, labels, ids



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
    else:
        data_cols = [None]*num_files

    if label_cols is not None:
        if type(label_cols) == int:
            label_cols = [label_cols]*num_files
        labels = []
    else:
        label_cols = [None]*num_files

    if id_cols is not None:
        if type(id_cols) == int:
            id_cols = [id_cols]*num_files
        ids = []
    else:
        id_cols = [None]*num_files

    return data, labels, ids, data_cols, label_cols, id_cols


def data_from_excel(filenames, data_cols=None, label_cols=None, id_cols=None, repeat_ids=True, first_row=1, limit=None, preprocess_func=None):
    '''
    Reads data from the filenames

    :param filenames: List of Excel filenames (List of strings)
    :param data_cols: List of location of data columns in each file  (List of int or int)
    :param label_cols: List of location of label columns in each file  (List of int or int)
    :param id_cols: List of location of id columns in each file  (List of int or int)
    :param repeat_ids: If False, data corresponding to already existing ids are concatenated (Boolean)
    :param first_row: Starts reading from specified row number (int)
    :param limit: Stops reading after specified number of lines have been read (int)
    :param preprocess_func: Applies preprocess_func to each row in a file

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

                    if limit is not None and count == limit:
                        break

                    #If label column is empty don't include it
                    if row[label_cols[file_num]].value is None:
                        continue

                    count += 1

                    #getting data, label and ids from each row and concatenating it
                    data, labels, ids = get_data(data_cols[file_num], label_cols[file_num], id_cols[file_num],
                                                 data, labels, ids, repeat_ids, lambda col: str(row[col].value))

    if preprocess_func is not None:
        for i in range(len(data)):
            data[i] = preprocess_func(data[i])

    return data, labels, ids


