import numpy as np
import matplotlib.pyplot as plt
import itertools
import os


#TODO: Fix this hideous mess I made
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
    negative_cases = {label: 0 for label in labels}
    predicted_negative_cases = {label: 0 for label in labels}
    false_positives = {label: 0 for label in labels}
    false_negatives = {label: 0 for label in labels}

    for i, label in enumerate(labels):
        positive_cases[label] = int(np.sum(cnf[i,:]))
        predicted_positive[label] = int(np.sum(cnf[:,i]))

        negative_cases_indices = np.ones_like(cnf)
        negative_cases_indices[i] = 0
        negative_cases[label] = int(np.sum(negative_cases_indices*cnf))

        false_negative_cases_indices = ~negative_cases_indices.astype(bool)
        false_negative_cases_indices[i,i] = False
        false_negatives[label] = int(np.sum(cnf*false_negative_cases_indices))

        false_positive_cases_indices = np.zeros_like(cnf)
        false_positive_cases_indices[:,i] = 1
        false_positive_cases_indices[i,i] = 0
        false_positives[label] = int(np.sum(cnf*false_positive_cases_indices))

        predicted_negative_cases_indices = np.ones_like(cnf)
        predicted_negative_cases_indices[:,i] = 0
        predicted_negative_cases[label] = int(np.sum(predicted_negative_cases_indices*cnf))

    return predicted_positive, positive_cases, predicted_negative_cases, negative_cases, false_positives, false_negatives

def get_classification_stats_capture(labels, preds, classifier_classes, negative_label="None"):
    pos_label = list(set(classifier_classes) - set([negative_label]))[0]

    predicted_positive_num = np.count_nonzero(np.not_equal(negative_label, np.array(preds, dtype=object)))
    positive_cases_num = np.count_nonzero(np.not_equal(negative_label, np.array(labels, dtype=object)))

    predicted_negative_num = np.count_nonzero(np.equal(negative_label, np.array(preds, dtype=object)))
    negative_cases_num = np.count_nonzero(np.equal(negative_label, np.array(labels, dtype=object)))

    predictions_at_negative_labels = preds[labels == negative_label]
    predictions_at_positive_labels = preds[labels != negative_label]

    false_positives_num = np.count_nonzero(np.not_equal(negative_label, np.array(predictions_at_negative_labels,
                                                                             dtype=object)))

    false_negatives_num = np.count_nonzero(np.equal(negative_label, np.array(predictions_at_positive_labels,
                                                                             dtype=object)))

    positive_cases = {pos_label: positive_cases_num, negative_label: negative_cases_num}
    predicted_positive = {pos_label: predicted_positive_num, negative_label: predicted_negative_num}
    negative_cases = {pos_label: negative_cases_num, negative_label: positive_cases_num}
    predicted_negative = {pos_label: predicted_negative_num, negative_label: predicted_positive_num}
    false_positives = {pos_label: false_positives_num, negative_label: false_negatives_num}
    false_negatives = {pos_label: false_negatives_num, negative_label: false_positives_num}

    return predicted_positive, positive_cases, predicted_negative, negative_cases, false_positives, false_negatives


def compute_ppv_accuracy_capture(labels, preds, classifier_classes, negative_label="None"):
    pos_label = list(set(classifier_classes) - set([negative_label]))[0]
    ppv_and_accuracy = {pos_label: {"ppv": 0, "npv": 0, "accuracy": 0, "num_correct": 0},
                        negative_label: {"ppv": 0, "npv": 0, "accuracy": 0, "num_correct": 0}}

    ppv = "nan"
    npv = "nan"

    num_correct = np.sum(preds == labels)

    negative_cases = labels[labels == negative_label]
    positive_cases = labels[labels != negative_label]

    predicted_positive = np.count_nonzero(np.not_equal(negative_label, np.array(preds, dtype=object)))
    predicted_negative = np.count_nonzero(np.equal(negative_label, np.array(preds, dtype=object)))

    predictions_at_negative_labels = preds[labels == negative_label]
    predictions_at_positive_labels = preds[labels != negative_label]

    true_positives = np.count_nonzero(np.equal(np.array(positive_cases, dtype=object), np.array(
        predictions_at_positive_labels, dtype=object)))

    true_negatives = np.count_nonzero(np.equal(np.array(negative_cases, dtype=object),
                                               np.array(predictions_at_negative_labels, dtype=object)))

    if predicted_positive > 0:
        ppv = true_positives/predicted_positive

    if predicted_negative > 0:
        npv = true_negatives/predicted_negative

    ppv_and_accuracy[pos_label]["ppv"] = ppv
    ppv_and_accuracy[pos_label]["npv"] = npv
    ppv_and_accuracy[pos_label]["accuracy"] = num_correct/len(labels)
    ppv_and_accuracy[pos_label]["num_correct"] = int(num_correct)
    ppv_and_accuracy[pos_label]["true_positives"] = int(true_positives)
    ppv_and_accuracy[pos_label]["sensitivity"] = int(true_positives)/positive_cases

    ppv_and_accuracy[negative_label]["ppv"] = npv
    ppv_and_accuracy[negative_label]["npv"] = ppv
    ppv_and_accuracy[negative_label]["accuracy"] = num_correct/len(labels)
    ppv_and_accuracy[negative_label]["num_correct"] = int(num_correct)
    ppv_and_accuracy[negative_label]["true_positives"] = int(true_positives)
    ppv_and_accuracy[negative_label]["sensitivity"] = int(true_positives)/positive_cases

    return ppv_and_accuracy

def compute_ppv_accuracy_ova(cnf, labels):

    ppv_and_accuracy = {label: {"ppv": 0, "accuracy": 0, "num_correct": 0, "npv": 0} for label in labels}

    for i, label in enumerate(labels):
        true_pos = cnf[i][i]

        pos_calls = cnf[:,i]
        neg_calls = np.copy(cnf)
        neg_calls[:,i] = 0

        true_neg = np.copy(cnf)
        true_neg[i,:] = 0
        true_neg[:,i] = 0

        accuracy = 1
        ppv = "nan"
        npv = "nan"

        if np.sum(cnf) > 0:
            accuracy = (true_pos + np.sum(true_neg))/np.sum(cnf)
            num_correct = true_pos + np.sum(true_neg)

        if np.sum(pos_calls) > 0:
            ppv = true_pos/sum(pos_calls)

        if np.sum(neg_calls) > 0:
            npv = np.sum(true_neg)/np.sum(neg_calls)

        ppv_and_accuracy[label]["ppv"] = ppv
        ppv_and_accuracy[label]["npv"] = npv
        ppv_and_accuracy[label]["accuracy"] = accuracy
        ppv_and_accuracy[label]["num_correct"] = int(num_correct)
        ppv_and_accuracy[label]["true_positives"] = int(true_pos)

        false_negatives = int(np.sum(neg_calls) - np.sum(true_neg))
        positive_cases = false_negatives + true_pos
        ppv_and_accuracy[label]["sensitivity"] = true_pos/positive_cases


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
