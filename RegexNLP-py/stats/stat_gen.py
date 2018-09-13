import os
from stats.basic import calculate_accuracy
from sklearn.metrics import confusion_matrix
from stats.basic import plot_confusion_matrix, get_classification_stats, compute_ppv_accuracy_ova, \
    compute_ppv_accuracy_capture, get_classification_stats_capture
from util.SpecialException import SpecialException

def get_failures(classifier_runner, cur_dataset, conf_path, print_output=True):
    try:
        failures_dict = {}
        try:
            cur_labels_list = sorted(list(set(classifier_runner.classifier.dataset[cur_dataset]["preds"].tolist()) |
                                      set(classifier_runner.classifier.dataset[cur_dataset]["labels"].tolist())))
        except TypeError:
            raise SpecialException("Error occurred when generating stats. Check label file to make sure all ids are unique.")
        accuracy, \
            incorrect_indices, num_correct = calculate_accuracy(classifier_runner.classifier.dataset[cur_dataset]["preds"],
                                                   classifier_runner.classifier.dataset[cur_dataset]["labels"])

        if print_output:
            print("\nAccuracy: ", accuracy)
            print("\nIds: ", classifier_runner.classifier.dataset[cur_dataset]["ids"])
            print("Predictions: ", classifier_runner.classifier.dataset[cur_dataset]["preds"])
            print("Labels: ", classifier_runner.classifier.dataset[cur_dataset]["labels"])

            print("\nIncorrect Ids: ", classifier_runner.classifier.dataset[cur_dataset]["ids"][incorrect_indices])
            print("Incorrect Predictions: ",
                  classifier_runner.classifier.dataset[cur_dataset]["preds"][incorrect_indices])
            print("Incorrect Labels: ", classifier_runner.classifier.dataset[cur_dataset]["labels"][incorrect_indices])

        classifier_type = classifier_runner.classifier_type.__name__
        classifier_classes = sorted(list(classifier_runner.classifier_parameters["regexes"]))

        if classifier_type == "CaptureClassifier":
            cnf_matrix = None

            ppv_and_accuracy = compute_ppv_accuracy_capture(
                classifier_runner.classifier.dataset[cur_dataset]["labels"],
                classifier_runner.classifier.dataset[cur_dataset]["preds"],
                classifier_classes, classifier_runner.classifier.negative_label)

            predicted_positive, positive_cases, predicted_negative_cases, negative_cases, \
            false_positives, false_negatives = get_classification_stats_capture(
                classifier_runner.classifier.dataset[cur_dataset]["labels"],
                classifier_runner.classifier.dataset[cur_dataset]["preds"],
                classifier_classes, classifier_runner.classifier.negative_label)

            cur_labels_list = classifier_classes

        else:

            cnf_matrix = confusion_matrix(classifier_runner.classifier.dataset[cur_dataset]["labels"],
                                          classifier_runner.classifier.dataset[cur_dataset]["preds"])
            ppv_and_accuracy = compute_ppv_accuracy_ova(cnf_matrix, cur_labels_list)
            predicted_positive, positive_cases, predicted_negative_cases, negative_cases, \
            false_positives, false_negatives = get_classification_stats(cnf_matrix, cur_labels_list)

        if print_output:
            print("Confusion Matrix: ")

            print("OVA PPV and Accuracy: ", ppv_and_accuracy)

            print("Number of Positive Predictions: ", predicted_positive)
            print("Actual number of Positive Cases: ", positive_cases)
            print("Number of Predicted Negative Cases: ", predicted_negative_cases)
            print("Actual Number of Negative Cases: ", negative_cases)

        for index in incorrect_indices:
            cur_patient_id = classifier_runner.classifier.dataset[cur_dataset]["ids"][index]
            cur_pred = classifier_runner.classifier.dataset[cur_dataset]["preds"][index]
            cur_label = classifier_runner.classifier.dataset[cur_dataset]["labels"][index]
            cur_match_obj = classifier_runner.classifier.dataset[cur_dataset]["matches"][index]
            cur_score = classifier_runner.classifier.dataset[cur_dataset]["scores"][index]
            cur_text = classifier_runner.classifier.dataset[cur_dataset]["data"][index]

            failures_dict[cur_patient_id] = {"label": cur_label, "data": cur_text, "pred": cur_pred,
                                             "matches": cur_match_obj, "score": cur_score}

        error_data = {"Predicted Positive": predicted_positive, "Positive Cases": positive_cases,
                      "Predicted Negative": predicted_negative_cases, "Negative Cases": negative_cases,
                      "False Positives": false_positives, "False Negatives": false_negatives,
                      "Confusion Matrix": cnf_matrix.tolist() if cnf_matrix is not None else [],
                      "OVA PPV and Accuracy": ppv_and_accuracy, "Ordered Labels": cur_labels_list,
                      "Negative Label": classifier_runner.classifier.negative_label,
                      "Classifier Type": classifier_type,
                      "Accuracy": accuracy,
                      "Num Correct": num_correct,
                      "Total Cases": num_correct + len(incorrect_indices)}

        if cnf_matrix is not None:
            plot_confusion_matrix(cnf_matrix, cur_labels_list, conf_path)
    except SpecialException as e:
        raise SpecialException(e)
    except Exception:
        raise SpecialException("Some error occurred during stat generation. Verify data file and label file.")

    return failures_dict, error_data
