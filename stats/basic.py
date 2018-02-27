import numpy as np

def calculate_accuracy(preds, labels):
    wrong_indices = np.nonzero(~(preds == labels))
    accuracy = np.sum(preds == labels)/len(labels)

    return accuracy, wrong_indices
