# -*- coding: utf-8 -*-
# @Author: Chloe
# @Date:   2019-07-17 11:28:05
# @Last Modified by:   Chloe
# @Last Modified time: 2019-07-17 12:39:05

import os
from datahandler import data_import as di

FAKE_DATA_PATH = os.path.abspath("../fake_data")
CSV_FILENAMES = [os.path.join(FAKE_DATA_PATH, "fake_notes.csv")]
EXCEL_FILENAMES = [os.path.join(FAKE_DATA_PATH, "fake_notes.xlsx")]


class TestDataFromCsv(object):

    def test_read_csv_file(self):
        data, labels, ids = di.data_from_csv(CSV_FILENAMES,
                                             data_cols=1,
                                             label_cols=None,
                                             id_cols=0)
        assert len(data) == 20
        assert len(ids) == 20

    def test_encoding(self):
        for encoding in [None, "utf-8", "latin-1"]:
            data, labels, ids = di.data_from_csv(CSV_FILENAMES,
                                                 data_cols=1,
                                                 label_cols=None,
                                                 id_cols=0,
                                                 encoding=encoding)
            assert len(data) == 20
            assert len(ids) == 20


class TestDataFromExcel(object):

    def test_read_excel_file(self):
        data, labels, ids = di.data_from_excel(EXCEL_FILENAMES,
                                               data_cols=1,
                                               label_cols=None,
                                               id_cols=0)
        assert len(data) == 20
        assert len(ids) == 20

    def test_encoding(self):
        for encoding in [None, "utf-8", "latin-1"]:
            data, labels, ids = di.data_from_excel(EXCEL_FILENAMES,
                                                   data_cols=1,
                                                   label_cols=None,
                                                   id_cols=0,
                                                   encoding=encoding)
            assert len(data) == 20
            assert len(ids) == 20
