import re
import openpyxl
import csv
from regex.regex import Regex
from regex.regex import SecondaryRegex
from time import time
import ast

def preprocess_data(data):
    '''
    Preprocesses datta

    :param data: data (string)

    :return: modified data
    '''

    data = data.replace('_x000D_', '').replace('\n#\n', '\n').replace('#', '\n').replace('\\n+','\n')
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

        #if repeat ids is false and id in ids, we want to concatenate the ids
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
        # print("-"*100)
        # print('NoneType has been found' if datum is None else datum)

        if concat_index is not None:
            data[concat_index] += "{}\n".format(preprocess_data(datum))
        else:
            data.append(preprocess_data(datum))

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


def data_from_excel(filenames, data_cols=None, label_cols=None, id_cols=None, repeat_ids=True, first_row=1, limit=None, preprocess_func=None, check_col=0):
    '''
    Reads data from the excel files

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

    print("Reading data from excel file...")

    count = 0
    for file_num, filename in enumerate(filenames):
        if limit is not None and count == limit:
            break

        workbook = openpyxl.load_workbook(filename, data_only=True, read_only=True)
        sheet_names = workbook.get_sheet_names()
        for sheet_name in sheet_names:
            #getting rows in worksheet
            cur_ws = workbook[sheet_name].rows
            for i, row in enumerate(cur_ws):
                if i >= first_row:
                   #If label column is empty don't include it
                    if row[check_col].value is None:
                        continue
                    count += 1
                    #getting data, label and ids from each row and concatenating it
                    data, labels, ids = get_data(data_cols[file_num], label_cols[file_num], id_cols[file_num],
                                                 data, labels, ids, repeat_ids, lambda col: str(row[col].value))
        end = time()
    if preprocess_func is not None:
        for i in range(len(data)):
            data[i] = preprocess_func(data[i])

    return data, labels, ids


def data_from_csv(filenames, data_cols=None, label_cols=None, id_cols=None, repeat_ids=True, first_row=1, limit=None, preprocess_func=None, check_col=0):
    '''
    Reads data from the csv files

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

    print("Reading data from csv file...")

    count = 0
    for file_num, filename in enumerate(filenames):
        if limit is not None and count == limit:
            break
        with open(filename, 'r', encoding='utf8') as csv_file:
            rows = csv.reader(csv_file, delimiter=',', quotechar='"')
            for i, row in enumerate(rows):
                if i >= first_row:
                    #If label column is empty don't include it
                    if row[check_col] == '':
                        continue

                    count += 1

                    #getting data, label and ids from each row and concatenating it
                    data, labels, ids = get_data(data_cols[file_num], label_cols[file_num], id_cols[file_num],
                                                 data, labels, ids, repeat_ids, lambda col: str(row[col]))

    if preprocess_func is not None:
        for i in range(len(data)):
            data[i] = preprocess_func(data[i])

    return data, labels, ids


def regexes_from_csv(filenames, regex_names, use_custom_score=False, all_matches=False, flags=[re.IGNORECASE]):
    '''
    Given a list of filenames containing regexes, returns a list of Regex objects

    :param filenames: A list of comma separated filenames
    :param regex_names: List of file nicknames. Must have the same number of elements as filenames
    :param use_custom_score: if True user specified scores are given when creating regexes

    :return: A list of Regex objects
    '''

    assert(len(filenames) == len(set(regex_names)))

    regexes = []
    classifier_type = None
    classifier_args = {}

    for file, nick_name in zip(filenames, regex_names):
        with open(file, 'r', encoding='utf8') as f:
            lines = csv.reader(f, delimiter=',', quotechar='"')
            for i, line in enumerate(lines):
                if i == 0 and line[0].startswith("!"):
                    classifier_type = line[0][1:]
                    if len(line) > 1:
                        for j in range(1, len(line) - 1, 2):
                            classifier_args[line[j]] = ast.literal_eval(line[j+1])
                    continue

                #Checking for invalid lines
                if len(line) < 1 and not line[0].startswith("#"):
                    print(line)
                    print("Empty line in file")
                    break

                #comment code
                if line[0].startswith("#"):
                    continue

                #Reading primary score and primary regex
                score = None if not use_custom_score else int(line[1])
                regex = line[0]

                secondary_regexes = []

                for j in range(2, len(line) - 2, 3):
                    pattern = line[j]
                    effect = line[j+1]
                    secondary_score = None if not use_custom_score else int(line[j+2])

                    secondary_regex = SecondaryRegex(name="sec_reg{}-{}-{}".format(len(regexes),len(secondary_regexes), nick_name),
                                                     regex=pattern, effect=effect, score=secondary_score, all_matches=all_matches, flags=flags)

                    secondary_regexes.append(secondary_regex)


                #creating regex objects
                cur_regex = Regex(name="reg{}-{}".format(len(regexes), nick_name), regex=regex, score=score,
                                  secondary_regexes=secondary_regexes, all_matches=True, flags=flags)

                regexes.append(cur_regex)

    return classifier_type, classifier_args, regexes
