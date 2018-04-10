import numpy as np
import matplotlib.pyplot as plt
import itertools
import os

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

def get_classification_stats(cnf, labels):
    positive_cases = {label: 0 for label in labels}
    predicted_positive = {label: 0 for label in labels}
    negative_cases = {"Not " + label: 0 for label in labels}
    predicted_negative_cases = {"Not " + label: 0 for label in labels}

    for i, label in enumerate(labels):
        positive_cases[label] = int(np.sum(cnf[i,:]))
        predicted_positive[label] = int(np.sum(cnf[:,i]))

        negative_cases_indices = np.ones_like(cnf)
        negative_cases_indices[i] = 0
        negative_cases["Not " + label] = int(np.sum(negative_cases_indices*cnf))

        predicted_negative_cases_indices = np.ones_like(cnf)
        predicted_negative_cases_indices[:,i] = 0
        predicted_negative_cases["Not " + label] = int(np.sum(predicted_negative_cases_indices*cnf))

    return predicted_positive, positive_cases, predicted_negative_cases, negative_cases

def compute_ppv_accuracy_ova(cnf, labels):

    ppv_and_accuracy = {label: {"ppv": 0, "accuracy": 0} for label in labels}
    total_accuracy = 0
    total_ppv = 0

    for i, label in enumerate(labels):
        true_pos = cnf[i][i]
        pos_calls = cnf[:,i]

        true_neg_bool = np.ones_like(cnf)
        true_neg_bool[i,:] = 0
        true_neg_bool[:,i] = 0
        masked = true_neg_bool*cnf
        true_neg = np.sum(masked)

        accuracy = 1
        ppv = "nan"

        if np.sum(cnf) > 0:
            accuracy = (true_pos + true_neg)/np.sum(cnf)
            total_accuracy += accuracy

        if np.sum(pos_calls) > 0:
            ppv = true_pos/sum(pos_calls)
            total_ppv += ppv

        ppv_and_accuracy[label]["ppv"] = ppv
        ppv_and_accuracy[label]["accuracy"] = accuracy


    return ppv_and_accuracy

def plot_confusion_matrix(cm, classes,
                          output_directory, normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(output_directory, title + '.png'))
    plt.clf()
