from classifier.tb import TB
from datahandler import data_import as di

if __name__ == "__main__":
    #Reading excel data
    data, labels, ids = di.data_from_excel()

    #Creating TB Classifier
    tb = TB("TB Classifier")
    tb.import_data(data, labels, ids)

    #Running TB Classifier
    tb.run_classifier()