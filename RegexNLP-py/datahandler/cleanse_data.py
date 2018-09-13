import openpyxl, csv
import re
import os


def cleanse_csv_file(load_filename, save_filename):
    saved_row = None
    row_to_append = None
    count = 0
    previous_b = ""
    append_row = False
    finished = False
    review_status = -1
    with open(load_filename + ".csv", 'r', encoding="utf8") as csv_file:
        rows = csv.reader(csv_file, delimiter=',', quotechar='"')

        with open(save_filename + ".csv",'w', newline='', encoding="utf8") as save_file:
            writer = csv.writer(save_file, delimiter=',', quotechar='"')
            i = 0
            while not finished:
                try:
                    row = next(rows)
                except StopIteration:
                    row = ["", "", ""]
                if i >= 1:
                    data = row[2].lower()
                    if previous_b != row[1] and i > 1:
                        append_row = True
                        row_to_append = saved_row
                        review_status = -1

                    if re.search(r'electronic[^ ]* signed', data) is not None:
                        review_status = 2
                        saved_row = row
                    elif re.search(r'unreviewed', data) is not None:
                        if review_status <= 0:
                            review_status = 0
                            saved_row = row
                    else:
                        if review_status <= 1:
                            review_status = 1
                            saved_row = row
                    previous_b = row[1]
                else:
                    append_row = True
                    row_to_append = row

                if row[0] == '' and i >= 1:
                    finished = True

                if append_row:
                    writer.writerow(row_to_append)
                    count += 1
                    append_row = False

                i += 1
    print(finished)
    print(i)
    print(count)


def cleanse_excel_file(load_filename, save_filename):
    workbook = openpyxl.load_workbook("{}.xlsx".format(load_filename), data_only=True, read_only=True)
    sheet_names = workbook.get_sheet_names()
    previous_b = ""
    review_status = -1
    save_wb = openpyxl.Workbook()
    save_ws = save_wb.active
    saved_row = None
    count = 0
    final = False
    for sheet_name in sheet_names:
        cur_ws = workbook[sheet_name]

        for i, row in enumerate(cur_ws.rows):
            append_row = False
            if i >= 1 and not row[0].value is None:
                data = str(row[2].value).lower()
                if previous_b != str(row[1].value):
                    append_row = True
                    review_status = -1
                if re.search(r'electronic[^ ]* signed',data) is not None:
                    review_status = 2
                    saved_row = row
                elif re.search(r'unreviewed',data) is not None:
                    if review_status <= 1:
                        review_status = 1
                        saved_row = row
                else:
                    if review_status <= 0:
                        review_status = 0
                        saved_row = row
            elif row[0].value is None:
                append_row = True
                final = True

            if append_row:
                save_ws.append(saved_row)
                count += 1
                if final:
                    break

    save_wb.save("{}.xlsx".format(save_filename))
    print(count)


if __name__ == "__main__":
    cur_path = "Z:\\LKS-CHART\\Projects\\NLP POC\\Study data\\TB\\dev\\Unlabeled"
    print(cur_path)
    cleanse_csv_file(os.path.join(cur_path, "Jane_list_unlabeled"), os.path.join(cur_path, "Jane_list_unlabeled(Clean)"))