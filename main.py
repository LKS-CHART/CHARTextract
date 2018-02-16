from classifier.tb import TB
from datahandler import data_import as di

if __name__ == "__main__":
    data, labels, ids = di.data_from_excel()
    tb = TB("TB Classifier")
    tb.run_classifier()