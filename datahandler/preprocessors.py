def replace_labels_with_required(label_of_interest, negative_label, labels_array):
    for i, label_list in enumerate(labels_array):
        labels_array[i] = label_of_interest if label_of_interest in label_list else negative_label

def replace_label_with_required(mapping_dict, labels_array):
    for i, label in enumerate(labels_array):
        labels_array[i] = mapping_dict[label] if label in mapping_dict else label

def replace_filter(filter_func, labels_array):
    for i, label in enumerate(labels_array):
        labels_array[i] = filter_func(label)
