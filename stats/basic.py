#TODO: Deprecate and just use pandas
import numpy as np

def calculate_accuracy(preds, labels):
    """Calculates the accuracy of the classifier given its predictions and labels
    
    Arguments:
        preds {list} -- List of predictions
        labels {list} -- List of labels
    
    Returns:
        accuracy {float} -- Accuracy of the classifier
        wrong_indices {list} -- List of indices that the classifier predicted incorrectly
    """

    wrong_indices = np.nonzero(~(preds == labels))[0]
    accuracy = np.sum(preds == labels)/len(labels)

    return accuracy, wrong_indices
