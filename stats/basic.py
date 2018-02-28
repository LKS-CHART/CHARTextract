import numpy as np

def calculate_accuracy(preds, labels):
    '''
    Calculates the accuracy of the classifier given its predictions and labels

    :param preds: List of predictions
    :param labels: List of labels

    :return: Accuracy of the classifier, a list of indices which the classifier got incorrect
    '''
    wrong_indices = np.nonzero(~(preds == labels))[0]
    accuracy = np.sum(preds == labels)/len(labels)

    return accuracy, wrong_indices
