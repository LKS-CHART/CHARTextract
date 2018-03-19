from variable_classifiers.base_runner import Runner, import_regexes, import_regex
from datahandler import data_import as di
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

if __name__ == "__main__":

    root = Tk()
    root.title("RegexNLP")

    #DATA UPLOAD

    data_label = Label(root, text="Data File")
    data_label.grid(column=0, row=0, sticky=W)

    data_text = Entry(root, width=40)
    data_text.grid(column=1, row=0)

    def file_btn_clicked():
        data_text.delete(0,'end')
        data_file = filedialog.askopenfile(title="Select file", filetype=[("CSV or Excel Files", ("*.csv", "*.xlsx"))])
        data_text.insert(END,data_file.name)

    data_upload = Button(root, text="Load", command=file_btn_clicked)
    data_upload.grid(column=2, row=0)

    data_checkvar = IntVar()
    data_checkbox = Checkbutton(text="Repeat Ids", variable=data_checkvar, onvalue=1, offvalue=0)
    data_checkbox.grid(column=3,row=0)

    data_col_label = Label(root, text="Data col")
    data_col_label.grid(column=0, row=1, sticky=W)

    data_col_text = Entry(root, width=10)
    data_col_text.grid(column=1, row=1, sticky=W)

    id_col_label = Label(root, text="ID col", anchor="w")
    id_col_label.grid(column=0, row=2, sticky=W)

    id_col_text = Entry(root, width=10)
    id_col_text.grid(column=1, row=2, sticky=W)


    #RULE UPLOAD

    rule_label = Label(root, text="Rules Folder")
    rule_label.grid(column=0, row=3)

    rule_text = Entry(root, width=40)
    rule_text.grid(column=1, row=3)

    def rule_btn_clicked():
        rule_text.delete(0,'end')
        rule_folder = filedialog.askdirectory()
        rule_text.insert(END,rule_folder)
        print(rule_folder)

    rule_upload = Button(root, text="Load", command=rule_btn_clicked)
    rule_upload.grid(column=2, row=3)
    root.geometry('435x200')

    print("HERE")
    root.mainloop()

    # mainframe = ttk.Frame(root, padding="")
    # w = tk.Label(root, text="Hello World!")
    # w.pack()
    # folder_pick = filedialog.askdirectory()
    # print(folder_pick)
    #
    # root.mainloop()

    # filename = args.filename
    # rules = args.rules_folder
    # repeat_ids = args.repeat_ids
    # data_col = args.data_col
    # id_col = args.id_col
    # line_start = args.line_start
    # training_mode = None if not args.training_mode else args.training_mode
    #
    # data, _, ids = di.data_from_csv([filename], data_cols=data_col, id_cols=id_col, repeat_ids=repeat_ids) if filename.endswith('.csv') \
    #     else di.data_from_excel([filename], data_cols=data_col, id_cols=id_col, repeat_ids=repeat_ids)
    #
    # if training_mode:
    #     l_id_col = int(training_mode[0])
    #     l_label_col = int(training_mode[1])
    #     l_first_row = int(training_mode[2])
    #     label_file = training_mode[3]
    #     train_percent = float(training_mode[4])
    #     train = True
    #
    #     _, temp_labels, temp_ids = di.data_from_excel([label_file], id_cols=l_id_col, label_cols=l_label_col, repeat_ids=repeat_ids, first_row=l_first_row, check_col=1)
    #
    #     labels = ["None"] * len(data)
    #     count = 0
    #     for i, data_id in enumerate(ids):
    #         if data_id in temp_ids:
    #             labels[i] = temp_labels[temp_ids.index(data_id)]
    #         else:
    #             count += 1
    #
    # rule_list = []
    # classifiers = []
    # classifiers_args = []
    #
    # rules = [(fname, os.path.join(rules, fname)) for fname in os.listdir(rules)]
    #
    # for rule_name, rule in rules:
    #     classifier_type, classifier_args, regexes_dict = import_regexes(rule) if os.path.isdir(rule) else import_regex(rule)
    #     classifier_args.update({"regexes": regexes_dict})
    #     classifiers_args.append(classifier_args)
    #     classifiers.append(classifier_type)
    #
    # # classifiers_args_list = [{"", "classifier_name"}]
    #
    # for classifier_args, classifier in zip(classifiers_args, classifiers):
    #     rule_classifier = Runner(classifier, **classifier_args)
    #
    #     if not train:
    #         rule_classifier.run(ids=ids, data=data)
    #     else:
    #         rule_classifier.run(ids=ids, data=data, labels=labels, train=train, train_percent=train_percent)
    #
    #     print(rule_classifier.classifier.dataset["train"]["preds"])

