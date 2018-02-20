from classifier.tb import TB
from datahandler import data_import as di
import os

if __name__ == "__main__":

    debug = False

    if not debug:
        print("Current data folder: {!r}\n".format(os.getenv('DATA_FOLDER')))
        filenames = [os.path.normpath(os.path.join(os.getenv('DATA_FOLDER'), 'smh.ctpa.140.xlsx'))]
        print("Files of interest: {!r}\n".format(filenames))
        #Reading excel data
        data, labels, ids = di.data_from_excel(filenames, data_cols=3, label_cols=12, id_cols=0, repeat_ids=False)
        print("\nTraining data tuples:\n")
        print(list(zip(data, labels, ids)))
    else:
        data, labels, ids = [],[],[]

    #Creating TB Classifier
    tb = TB("TB Classifier 1")
    tb.import_data(data, labels, ids)
    train_ids, valid_ids = tb.create_train_and_valid(.5, 0)
    ids = {"train": train_ids, "valid": valid_ids}

    #Running TB Classifier
    tb.run_classifier()