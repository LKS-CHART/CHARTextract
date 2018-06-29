import re
import openpyxl
import csv
from regex.regex import Regex
from time import time
import ast
import os
import json

def preprocess_data(data):
    """Preprocesses data
    
    Arguments:
        data {string} -- data to be preprocessed
    
    Returns:
        modified_data {string} -- modified data
    """
    #print("HER")
    data = data.replace('_x000D_', '').replace('\n#\n', '\n').replace('#', '\n').replace('\\n','\n')
    #data, num_subs = re.subn(re.compile('nofilling',re.IGNORECASE), 'no filling', data)
    data, _ = re.subn(r'\bM.{1,2}\.', '', data)
    data, _ = re.subn(r'\bD.{1,2}\.', '', data)
    data, _ = re.subn(r'(\d)?\.(\d) ?cm\b', r'\1\2 mm', data)
    #data, num_subs = re.subn(r'\s{3,}', " ", data)
    data = data.replace(' St.', ' St')
    data = data.replace('D.O.B.', 'DOB')
    return data


def get_labeled_data(ids_list, data_list, label_file, l_id_col=1, l_label_col=None, l_first_row=3,
                     label_func=None):
    """
    :param ids_list:
    :param data_list:
    :param label_file:
    :param l_id_col:
    :param l_label_col:
    :param l_first_row:
    :param label_func:
    :return:
    """

    new_data_list = []
    new_labels_list = []
    new_ids_list = []

    local_data_loader = data_from_csv if label_file.endswith('.csv') else data_from_excel
    # TODO: accordingly increment/decrement l_id_col, l_label_col, l_first_row, check_col depending on filetype
    _, temp_labels, temp_ids = local_data_loader([label_file], id_cols=l_id_col, label_cols=l_label_col,
                                          repeat_ids=False, first_row=l_first_row, check_col=1)

    new_list = []
    for i, data_id in enumerate(ids_list):
        if data_id in temp_ids:
            # temp_ids must be unique
            new_list.append([temp_labels[temp_ids.index(data_id)], data_list[i], data_id])

    new_list = sorted(new_list, key=lambda j: j[2])

    for each in new_list:
        new_labels_list.append(each[0])
        new_data_list.append(each[1])
        new_ids_list.append(each[2])

    if label_func:
        label_func(new_labels_list)

    return new_ids_list, new_data_list, new_labels_list


def get_data(data_col, label_col, id_col, data, labels, ids, repeat_ids, row_process_func):
    """Gets data, label and id from a row
    
    Arguments:
        data_col {int} -- data column number
        label_col {int} -- label column number
        id_col {int} -- id column number
        data {list} -- list of data so far
        labels {list} -- list of labels so far
        ids {list} -- list of ids so far
        repeat_ids {boolean} -- if False, data is concatenated
        row_process_func {function} -- function that extracts a value from a row
    
    Returns:
        data {list} -- list of data
        labels {list} -- list of labels
        ids {list} -- list of ids
    """
    concat_index = None
    # id_col which is a list
    if id_col is not None:
        cur_id = row_process_func(id_col)

        #if repeat ids is false and id in ids, we want to concatenate the ids
        if not repeat_ids and cur_id in ids:
            concat_index = ids.index(cur_id)
        else:
            ids.append(cur_id)

    if label_col is not None:
        #If we are concatenating data (i.e repeat_ids = False), use all the diagnoses
        cur_label = []
        for actual_label_col in label_col:
            val = row_process_func(actual_label_col)
            val = "None" if not val else val
            cur_label.append(val)
        if concat_index is not None:
            if type(labels[concat_index]) == list:
                labels[concat_index].extend(cur_label)
            else:
                labels[concat_index] = [labels[concat_index]].extend(cur_label)
        else:
            if len(cur_label) == 1:
                labels.append(cur_label[0])
            else:
                labels.append(cur_label)

    if data_col is not None:
        data_string = row_process_func(data_col[0])
        for i in range(1, len(data_col)):
            data_string += "\n{}".format(row_process_func(data_col[i]))
        # print("-"*100)
        # print('NoneType has been found' if datum is None else datum)

        if concat_index is not None:
            data[concat_index] += "{}\n".format(preprocess_data(data_string))
        else:
            data.append(preprocess_data(data_string))

    return data, labels, ids


def _data_helper(num_files, data_cols=None, label_cols=None, id_cols=None):
    """Initializes data, labels, ids, data_cols, label_cols, id_cols as list
    
    Arguments:
        num_files {int} -- number of files
    
    Keyword Arguments:
        data_cols {int or list of int} -- location of data (default: {None})
        label_cols {int of list of ints} -- location of labels (default: {None})
        id_cols {int or list of ints} -- location of ids (default: {None})
    
    Returns:
        data {list} -- empty data list
        labels {list} -- empty labels list
        ids {list} -- empty ids list
        data_cols {list} -- location of data
        label_cols {list} -- location of labels
        id_cols {list} -- location of ids
    """
    data = None
    labels = None
    ids = None

    if data_cols is not None:
        #duplicating int. i.e assuming that every file has the same data col
        if type(data_cols) == int:
            data_cols = [[data_cols]]*num_files
        else:
            data_cols = [data_cols] * num_files
        data = []
    else:
        data_cols = [None]*num_files

    if label_cols is not None:
        if type(label_cols) == int:
            label_cols = [[label_cols]]*num_files
        else:
            label_cols = [label_cols] * num_files
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
    """Reads data from excel files
    
    Arguments:
        filenames {list of string} -- List of Excel filenames
    
    Keyword Arguments:
        data_cols {list of int or int} -- List of location of data columns in each file (default: {None})
        label_cols {list of int or int} -- List of location of label columns in each file (default: {None})
        id_cols {list of int or int} -- List of location of id columns in each file (default: {None})
        repeat_ids {bool} -- If False, data corresponding to already existing ids are concatenated (default: {True})
        first_row {int} -- Starts reading from specified row number (default: {1})
        limit {int} -- Stops reading after specified number of lines have been read (default: {None})
        preprocess_func {function} -- Applies preprocess function to each row in a file (default: {None})
        check_col {int} -- Data column to check whether to continue evaluation (default: {0})
    
    Returns:
        data {list} -- list of data
        labels {list} -- list of labels
        ids {list} -- list of ids
    """

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
                   #If check column is empty don't include it
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

def import_pwds(filenames, pwd_names=None):
    """Imports personal word dictionaries
    
    Arguments:
        filenames {list of str} -- list of filepaths
    
    Keyword Arguments:
        pwd_names {string} -- personal word dictionary names (default: {None})
    
    Returns:
        pwds {dict} -- Personal word dictionary which is a dictionary which maps pwd_name -> list of words
    """

    pwds = {}
    pwd_names = [(lambda f: f.split(os.sep)[-1].split(".")[0])(file) for file in filenames] if not pwd_names else pwd_names

    for file, pwd_name in zip(filenames, pwd_names):
        pwds[pwd_name] = []
        with open(file, 'r', encoding='utf8') as csv_file:
            rows = csv.reader(csv_file, delimiter=',', quotechar='"')
            pwds[pwd_name] = [word.strip() for row in rows for word in row]

    return pwds

def data_from_csv(filenames, data_cols=None, label_cols=None, id_cols=None, repeat_ids=True, first_row=1, limit=None,
                  preprocess_func=None, check_col=0):

    """Reads data from excel files
    
    Arguments:
        filenames {list of string} -- List of Excel filenames
    
    Keyword Arguments:
        data_cols {list of int or int} -- List of location of data columns in each file (default: {None})
        label_cols {list of int or int} -- List of location of label columns in each file (default: {None})
        id_cols {list of int or int} -- List of location of id columns in each file (default: {None})
        repeat_ids {bool} -- If False, data corresponding to already existing ids are concatenated (default: {True})
        first_row {int} -- Starts reading from specified row number (default: {1})
        limit {int} -- Stops reading after specified number of lines have been read (default: {None})
        preprocess_func {function} -- Applies preprocess function to each row in a file (default: {None})
        check_col {int} -- Data column to check whether to continue evaluation (default: {0})
    
    Returns:
        data {list} -- list of data
        labels {list} -- list of labels
        ids {list} -- list of ids
    """

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

#TODO: Probably shouldn't have default mutable args. Change later
def regexes_from_csv(filename, use_custom_score=False, all_matches=False, flags=[re.IGNORECASE]):
    """Given a file containing regexes, returns the classifier name, its arguments, class name, list of Regex objects
    
    Arguments:
        filename {string} -- Regex filename
    
    Keyword Arguments:
        use_custom_score {bool} -- If True, use user defined score (default: {False})
        all_matches {bool} -- If True, regex will return all matches (default: {False})
        flags {list} -- List of regex flags (default: {[re.IGNORECASE]})
    
    Raises:
        Exception -- Raises exception if label name not specified at the start of the file
    
    Returns:
        classifier_type {String} -- The type of classifier specified in the file if any
        classifier_args {list} -- List of classifier arguments specified in the file if any
        class_name {String} -- Name of class
        regexes {list} -- List of Regex objects
    """

    regexes = []
    classifier_type = None
    classifier_args = {}
    class_name = None

    with open(filename, 'r', encoding='utf8') as f:
        lines = csv.reader(f, delimiter=',', quotechar='"')
        for i, line in enumerate(lines):
            if i == 0:
                if not line[0].startswith("!"):
                    raise Exception("Rule file requires label name at start of file. Specify as !label_name")

                #Name of class
                class_name = line[0][1:]
                if len(line) > 1:
                    #Type of classifier
                    classifier_type = line[1]
                    #Looping through remaining pairs of arg_name, arg_val and evaluating using ast.literal_eval
                    for j in range(2, len(line) - 1, 2):
                        print(line[j+1])
                        # TODO: Make safer
                        classifier_args[line[j]] = ast.literal_eval(line[j+1])

                continue

            #blank line check
            if len(line) == 0:
                continue

            #comment code
            if line[0].startswith("#"):
                continue

            #Reading primary score and primary regex
            score = None if not use_custom_score else int(line[1])
            regex = line[0]

            secondary_regexes = []

            #Creating list of secondary regexes for the primary regex
            for j in range(2, len(line) - 2, 3):
                pattern = line[j]
                effect = line[j+1]
                secondary_score = None if not use_custom_score else int(line[j+2])

                secondary_regex = Regex(name="sec_reg{}-{}-{}".format(len(regexes),len(secondary_regexes), class_name),
                                        regex=pattern, effect=effect, score=secondary_score, all_matches=all_matches, flags=flags, secondary_regexes=[])

                secondary_regexes.append(secondary_regex)


            #Creating regex
            cur_regex = Regex(name="reg{}-{}".format(len(regexes), class_name), regex=regex, score=score, effect='p',
                              secondary_regexes=secondary_regexes, all_matches=all_matches, flags=flags)


            regexes.append(cur_regex)

    return classifier_type, classifier_args, class_name, regexes

#New json format
def regexes_from_json2(filename, use_custom_score=False):
    with open(filename, 'r') as f:
        data = json.load(f)
        classifier_type = data["Classifier Type"] if "Classifier Type" in data else "RegexClassifier"
        all_matches = data["All Matches"] if "All Matches" in data else False

        classifier_args = data["Classifier Args"] if "Classifier Args" in data else {}

        if "Rules" in data:
            if not data["Rules"]:
                raise Exception("No classes found in file. Rule file requires a label name e.g Yes")
            for name in data["Rules"]:
                class_name = name
                regexes = []
                for rule in data["Rules"][name]:
                    score = None if not use_custom_score else rule["Primary"]["Score"]
                    primary_pattern = rule["Primary"]["Rule"]

                    secondary_regexes = []

                    if "Case Sensitive" in rule:
                        flags = [re.IGNORECASE] if not rule["Case Sensitive"] else None
                    else:
                        flags = None

                    for secondary_rule in rule["Secondary"]:
                        secondary_score = None if not use_custom_score else secondary_rule["Score"]
                        secondary_pattern = secondary_rule["Rule"]

                        effect = secondary_rule["Type"]

                        if "Modifier" in secondary_rule:
                            effect += secondary_rule["Modifier"]

                        if "Case Sensitive" in secondary_rule:
                            flags_secondary = [re.IGNORECASE] if not secondary_rule["Case Sensitive"] else None
                        else:
                            flags_secondary = None

                        #Remember to never do what is under this line ever again
                        # effect = secondary_rule["Type"] + secondary_rule["Modifier"] \
                        #     if "Modifier" in secondary_rule else ""

                        secondary_regex = Regex(name="sec_reg{}-{}-{}".format(len(regexes),len(secondary_regexes),
                                                                              class_name), regex=secondary_pattern, effect=effect, score=secondary_score,
                                                all_matches=all_matches, flags=flags_secondary, secondary_regexes=[])

                        secondary_regexes.append(secondary_regex)

                    primary_regex = Regex(name="reg{}-{}".format(len(regexes), class_name), regex=primary_pattern,
                                          score=score, effect='p', secondary_regexes=secondary_regexes,
                                          all_matches=all_matches, flags=flags)

                    regexes.append(primary_regex)

                yield classifier_type, classifier_args, class_name, regexes


#Old json format

def read_classifier_settings(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        classifier_type = data["Classifier Type"] if "Classifier Type" in data else "RegexClassifier"
        classifier_args = data["Classifier Args"] if "Classifier Args" in data else {}

    return classifier_type, classifier_args


def regexes_from_json(filename, use_custom_score=False, all_matches=False, flags=[re.IGNORECASE]):
    regexes = []
    class_name = None
    classifier_args = {}

    with open(filename, 'r') as f:
        data = json.load(f)
        classifier_type = data["Classifier Type"] if "Classifier Type" in data else "RegexClassifier"
        all_matches = data["All Matches"] if "All Matches" in data else False

        if "Case Sensitive" in data:
            flags = [re.IGNORECASE] if not data["Case Sensitive"] else None
        else:
            flags = None

        if "Name" not in data:
            raise Exception("Rule file requires a label name.")
        else:
            class_name = data["Name"]

        classifier_args = data["Classifier Args"] if "Classifier Args" in data else {}

        if "Rules" in data:
            for rule in data["Rules"]:
                score = None if not use_custom_score else rule["Primary"]["Score"]
                primary_pattern = rule["Primary"]["Rule"]

                secondary_regexes = []

                for secondary_rule in rule["Secondary"]:
                    secondary_score = None if not use_custom_score else secondary_rule["Score"]
                    secondary_pattern = secondary_rule["Rule"]

                    effect = secondary_rule["Type"]

                    if "Modifier" in secondary_rule:
                        effect += secondary_rule["Modifier"]

                    #Remember to never do what is under this line ever again
                    # effect = secondary_rule["Type"] + secondary_rule["Modifier"] \
                    #     if "Modifier" in secondary_rule else ""

                    secondary_regex = Regex(name="sec_reg{}-{}-{}".format(len(regexes),len(secondary_regexes),
                                            class_name), regex=secondary_pattern, effect=effect, score=secondary_score,
                                            all_matches=all_matches, flags=flags, secondary_regexes=[])

                    secondary_regexes.append(secondary_regex)

                primary_regex = Regex(name="reg{}-{}".format(len(regexes), class_name), regex=primary_pattern,
                                       score=score, effect='p', secondary_regexes=secondary_regexes,
                                       all_matches=all_matches, flags=flags)

                regexes.append(primary_regex)

    return classifier_type, classifier_args, class_name, regexes
