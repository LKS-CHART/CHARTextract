def replace_labels_with_required(label_of_interest, negative_label, labels_array):
    for i, label_list in enumerate(labels_array):
        labels_array[i] = label_of_interest if label_of_interest in label_list else negative_label


def replace_label_with_required(mapping_dict, labels_array):
    for i, label in enumerate(labels_array):
        labels_array[i] = mapping_dict[label] if label in mapping_dict else label


def replace_filter(filter_func, labels_array):
    for i, label in enumerate(labels_array):
        labels_array[i] = filter_func(label)


def replace_filter_by_label(label_of_interest, negative_label, exact_match=False, labels_array=None):
    for i, label in enumerate(labels_array):
        if exact_match:
            labels_array[i] = label_of_interest if label.find(label_of_interest) >= 0 else negative_label
        else:
            labels_array[i] = label_of_interest if label_of_interest == label else negative_label

        
def convert_repeated_data_to_sublist(repeated_ids, repeated_data=None, repeated_labels=None):
    repeated_dict = {}
    repeated_ids_list = []

    if repeated_data is None:
        repeated_data = [None]*len(repeated_ids)

    if repeated_labels is None:
        repeated_labels = [None]*len(repeated_ids)

    for repeated_id, repeated_label, repeated_datum in zip(repeated_ids, repeated_labels, repeated_data):
        if repeated_id not in repeated_dict:
            repeated_dict[repeated_id] = {"data": [], "labels": []}
            repeated_dict[repeated_id]["data"] = [repeated_datum]
            repeated_dict[repeated_id]["labels"] = [repeated_label]
            repeated_ids_list.append(repeated_id)
        else:
            repeated_dict[repeated_id]["data"].append(repeated_datum)
            repeated_dict[repeated_id]["labels"].append(repeated_label)

    repeated_data_list = [repeated_dict[unique_id]["data"] for unique_id in repeated_ids_list]
    repeated_labels_list = [repeated_dict[unique_id]["labels"] for unique_id in repeated_ids_list]

    return repeated_ids_list, repeated_data_list, repeated_labels_list
