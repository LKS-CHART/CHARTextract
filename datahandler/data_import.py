import re
import openpyxl
import csv

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


    return data, labels, ids

