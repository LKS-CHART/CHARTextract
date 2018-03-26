from variable_classifiers.base_runner import Runner
from datahandler import data_import as di
import os
from tkinter import *
from tkinter import filedialog

def import_regex(regex_file):

    regexes = {}

    classifier_type, classifier_args, class_name, regexes[class_name] = di.regexes_from_csv(regex_file, use_custom_score=True)

    classifier_type = "RegexClassifier" if not classifier_type else classifier_type

    return classifier_type, classifier_args, regexes

def import_regexes(regex_directory):
    file_names = os.listdir(regex_directory)
    regex_filenames = [os.path.join(regex_directory, fname) for fname in file_names]

    regexes = {}

    classifier_type = None
    classifier_args = {}

    for file in regex_filenames:
        _classifier_type, _classifier_args, _class_name, regexes[_class_name] = di.regexes_from_csv(file, use_custom_score=True)
        classifier_type = _classifier_type if _classifier_type else classifier_type
        classifier_args = _classifier_args if _classifier_args else classifier_args

    classifier_type = "RegexClassifier" if not classifier_type else classifier_type

    return classifier_type, classifier_args, regexes

if __name__ == "__main__":

    root = Tk()
    root.title("RegexNLP")


    filename = StringVar()
    rules = StringVar()
    repeat_ids = IntVar()
    id_col = StringVar()
    data_col = StringVar()
    line_start = StringVar()

    def rule_btn_clicked():
        rule_text.delete(0,'end')
        rule_folder = filedialog.askdirectory()
        rule_text.insert(END,rule_folder)
        print(rule_folder)

    #RULE UPLOAD

    rule_label = Label(root, text="Rules Folder")
    rule_label.grid(column=0, row=0)

    rule_text = Entry(root, width=40, textvariable=rules)
    rule_text.grid(column=1, row=0)
    rule_text.insert(END,'Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/rules')

    rule_upload = Button(root, text="Load", command=rule_btn_clicked)
    rule_upload.grid(column=2, row=0)

    #DATA UPLOAD

    data_label = Label(root, text="Data File")

    data_label.grid(column=0, row=1, sticky=W)

    data_text = Entry(root, width=40, textvariable=filename)
    data_text.grid(column=1, row=1)
    data_text.insert(END, 'Z:/LKS-CHART/Projects/NLP POC/Study data/TB/dev/NLP Study (TB Clinic) Cohort 2 (really cleansed).csv')

    def file_btn_clicked():
        data_text.delete(0,'end')
        data_file = filedialog.askopenfile(title="Select file", filetype=[("CSV or Excel Files", ("*.csv", "*.xlsx"))])
        data_text.insert(END,data_file.name)

    data_upload = Button(root, text="Load", command=file_btn_clicked)
    data_upload.grid(column=2, row=1)

    data_checkvar = IntVar()
    data_checkbox = Checkbutton(text="Repeat Ids", variable=repeat_ids, onvalue=1, offvalue=0)
    data_checkbox.grid(column=3, row=1)

    #DATA PARAMETERS

    data_col_label = Label(root, text="Data col")
    data_col_label.grid(column=0, row=2, sticky=W)

    data_col_text = Entry(root, width=10, textvariable=data_col)
    data_col_text.insert(END,'2')
    data_col_text.grid(column=1, row=2, sticky=W)

    id_col_label = Label(root, text="ID col", anchor="w")
    id_col_label.grid(column=0, row=3, sticky=W)

    id_col_text = Entry(root, width=10, textvariable=id_col)
    id_col_text.insert(END,'0')
    id_col_text.grid(column=1, row=3, sticky=W)

    line_label = Label(root, text="Line start", anchor="w")
    line_label.grid(column=0, row=4, sticky=W)

    line_col_text = Entry(root, width=10, textvariable=line_start)
    line_col_text.insert(END,'1')
    line_col_text.grid(column=1, row=4, sticky=W)

    #RUN SCRIPT

    def run_script():
        str_filename = filename.get()
        str_rules = rules.get()
        bool_repeat_ids = repeat_ids.get() == 1
        int_line_start = int(line_start.get()) if line_start.get() else 1
        int_id_col = int(id_col.get()) if id_col.get() else 0
        int_data_col = int(data_col.get()) if data_col.get() else 1


        data, _, ids = di.data_from_csv([str_filename], data_cols=int_data_col, first_row=int_line_start, id_cols=int_id_col, repeat_ids=bool_repeat_ids) if str_filename.endswith('.csv') \
            else di.data_from_excel([str_filename], data_cols=int_data_col, id_cols=int_id_col, repeat_ids=bool_repeat_ids, first_row=int_line_start)

        classifiers = []
        classifiers_args = []

        rule_tups = [(fname, os.path.normpath(os.path.join(str_rules, fname))) for fname in os.listdir(str_rules)]

        for rule_name, rule in rule_tups:
            classifier_type, classifier_args, regexes_dict = import_regexes(rule) if os.path.isdir(rule) else import_regex(rule)
            print(regexes_dict)
            classifier_args.update({"regexes": regexes_dict})
            classifiers_args.append(classifier_args)
            classifiers.append(classifier_type)

        for classifier_args, classifier in zip(classifiers_args, classifiers):
            rule_classifier = Runner(classifier, **classifier_args)
            rule_classifier.run(ids=ids, data=data)
            print(rule_classifier.classifier.dataset["test"]["preds"])

    run = Button(root, text="RUN", command=run_script)
    run.grid(column=0, row=5, sticky=W)

    root.mainloop()

