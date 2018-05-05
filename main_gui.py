from variable_classifiers.base_runner import Runner
from datahandler import data_import as di
from variable_classifiers.base_runner import Runner
from datahandler import data_import as di
import os
from datahandler.helpers import import_regex, import_regexes
from web.report_generator import generate_error_report
from stats.basic import calculate_accuracy
from sklearn.metrics import confusion_matrix
from stats.basic import plot_confusion_matrix, get_classification_stats, compute_ppv_accuracy_ova, \
    compute_ppv_accuracy_capture, get_classification_stats_capture

from functools import partial

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

def create_regex_based_classifier(rule_path=None):
    """Creates a Regex based classifier Runner object which is later used to run the classifier

    Arguments:
        rule_path {String} -- Path to the rule directory (in the case of multiclass classification)
            or a rule file (in the case of single class classificatoin)
        ids_list {list} -- List of ids
        data_list {list} -- List of data (string) for each id

    Keyword Arguments:
        labels_list {list} -- List of labels (default: {None})
        training_mode {bool} -- Whether to run the classifier in training mode. If in training mode creates training
            and validation datasets (default: {False})
        l_id_col {int} -- Column in which label_file's ids are located starting from 0 (default: {None})
        l_label_col {int} -- Column in which label_file's labels are located starting from 0 (default: {None})
        l_first_row {int} -- From which row to start reading the data (default: {None})
        label_file {String} -- Path pointing to label file (default: {None})
        repeat_ids {bool} -- If False, ids are not considered unique and the data is appended (default: {False})
        train_percent {float} -- Percentage of training examples (default: {0.6})

    Returns:
        classifier_runner {Runner} -- Returns a Runner object which is used to run the classifier
    """

    # Import rule directory or rule file and updating classifier_args
    # Creating the Runner object with specified classifier_args

    runner = None

    try:
        classifier_type, classifier_args, regexes_dict = import_regexes(rule_path) \
            if os.path.isdir(rule_path) else import_regex(rule_path)
        classifier_args.update({"regexes": regexes_dict})
        runner = Runner(classifier_type, **classifier_args)

    except(Exception):
        print("Error loading ", rule_path)

    return runner

def load_file(location_var):
    opened_file = filedialog.askopenfile(title="Select a file", filetype=[("CSV or Excel Files", ("*.csv", "*.xlsx"))])
    location_var.set(opened_file.name)

def load_folder(location_var, func, *args):
    opened_folder = filedialog.askdirectory(title="Select a folder")
    location_var.set(opened_folder)

    func(*args)

def load_rules(rule_folder, tree, runner_list):
    tree.delete(*tree.get_children())

    runner_copy = []
    for rule in os.listdir(rule_folder.get()):
        rule_file = os.path.join(rule_folder.get(), rule)
        rule_name = rule.split(sep=".txt")[0]
        tree.insert('', 'end', text=rule_name)
        classifier_runner = create_regex_based_classifier(rule_file)
        runner_copy.append(classifier_runner)

    runner_list = runner_copy.copy()

def edit_tree(item):
    print("EDITING TREE")

    selected_row = rules_view_tree.focus()

    rvt_item = partial(rules_view_tree.item, selected_row)

    values = rvt_item()
    selected_row_rule.set("Editing Label Column for " + values["text"])

    # rvt_item(values=('test'))

    selected_row_label_col.set(rvt_item(option="values"))

def edit_label_col(*args):
    print(args)
    print(rules_view_tree.focus())
    rules_view_tree.item(rules_view_tree.focus(), values=selected_label_col_text.get())

def run_rules():
    pass

if __name__ == "__main__":

    root = Tk()
    root.title("RegexNLP")

    content = ttk.Frame(root, padding="3 3 3 12", width=300, height=300)
    content.grid(column=0, row=0, sticky=(N, S, E, W))

    rule_folder = StringVar()
    data_file = StringVar()
    data_cols = StringVar()
    label_file = StringVar()
    data_id_col = IntVar()
    label_id_col = IntVar()
    selected_row_label_col = StringVar()
    selected_row_rule = StringVar()

    selected_row_rule.set("Editing Label Column for")

    runners_list = []

    # rule_folder.set(os.path.join(os.getenv('TB_DATA_FOLDER'), 'rules', 'tb_rules'))
    # data_file.set(os.path.join(os.getenv('TB_DATA_FOLDER'), 'CombinedData.csv'))

    rules_view_tree = ttk.Treeview(content)
    rules_view_tree['columns'] = ('labelcols')
    rules_view_tree.heading("#0", text='Rules', anchor=W)
    rules_view_tree.column("#0", anchor=W)
    rules_view_tree.heading('labelcols', text="Label Column Numbers")
    rules_view_tree.column('labelcols', anchor='center', width=200)
    rules_view_tree.grid(row=8, columnspan=5, sticky=(N, S, E, W))
    rules_view_tree.bind('<<TreeviewSelect>>', edit_tree)

    rule_folder_label = ttk.Label(content, text="Rule Folder: ").grid(column=0, row=0, sticky=W)
    rule_folder_text = ttk.Entry(content, textvariable=rule_folder, width=30).grid(column=1, row=0, columnspan=3,
                                                                                   sticky=(E, W))

    rule_folder_button = ttk.Button(content, text="Open Folder", command=partial(load_folder, rule_folder, load_rules,
                                                                                 *[rule_folder, rules_view_tree,
                                                                                   runners_list])).grid(column=4, row=0,
                                                                                                        sticky=W)

    # load_rules(rule_folder, rules_view_tree, runners_list)

    data_file_label = ttk.Label(content, text="Data File: ").grid(column=0, row=1, sticky=W)
    data_file_text = ttk.Entry(content, textvariable=data_file).grid(column=1, row=1, columnspan=3, sticky=(E, W))
    data_file_button = ttk.Button(content, text="Open File", command=partial(load_file, data_file)).grid(column=4,
                                                                                                         row=1,
                                                                                                         sticky=W)

    data_columns_label = ttk.Label(content, text="Data Columns: ").grid(column=0, row=2, sticky=W)
    data_columns_text = ttk.Entry(content, textvariable=data_cols).grid(column=1, row=2, columnspan=3, sticky=(E, W))

    data_id_label = ttk.Label(content, text="Data ID Column: ").grid(column=0, row=3, sticky=W)
    data_id_text = ttk.Entry(content, textvariable=data_id_col).grid(column=1, row=3, columnspan=3, sticky=(E, W))

    label_file_label = ttk.Label(content, text="Label File: ").grid(column=0, row=4, sticky=W)
    label_file_text = ttk.Entry(content, textvariable=label_file).grid(column=1, row=4, columnspan=3, sticky=(E, W))
    label_file_button = ttk.Button(content, text="Open File", command=partial(load_file, label_file)).grid(column=4,
                                                                                                           row=4,
                                                                                                           sticky=W)

    content.grid_rowconfigure(5, minsize=20)

    run_button = ttk.Button(content, text="Run").grid(column=0, row=6, sticky=W)

    content.grid_rowconfigure(7, minsize=10)

    selected_label_col_label = ttk.Label(content, textvariable=selected_row_rule).grid(column=0, columnspan=2, row=9,
                                                                                       sticky=W)
    selected_label_col_text = ttk.Entry(content, textvariable=selected_row_label_col)
    selected_label_col_text.bind("<Return>", edit_label_col)

    selected_label_col_text.grid(column=3, row=9, sticky=(E, W))


    # def run_script():
    #     str_filename = filename.get()
    #     str_rules = rules.get()
    #     bool_repeat_ids = repeat_ids.get() == 1
    #     int_line_start = int(line_start.get()) if line_start.get() else 1
    #     int_id_col = int(id_col.get()) if id_col.get() else 0
    #     int_data_col = int(data_col.get()) if data_col.get() else 1
    #
    #
    #     data, _, ids = di.data_from_csv([str_filename], data_cols=int_data_col, first_row=int_line_start, id_cols=int_id_col, repeat_ids=bool_repeat_ids) if str_filename.endswith('.csv') \
    #         else di.data_from_excel([str_filename], data_cols=int_data_col, id_cols=int_id_col, repeat_ids=bool_repeat_ids, first_row=int_line_start)
    #
    #SCALING STUFF: LOOK AT LATER

    # root.columnconfigure(0, weight=1)
    # root.rowconfigure(0, weight=1)
    # root.rowconfigure(0, weight=1)
    # content.columnconfigure(0, weight=1)
    # content.rowconfigure(0, weight=1)
    # content.columnconfigure(1, weight=1)
    # content.rowconfigure(1, weight=1)

    root.mainloop()

