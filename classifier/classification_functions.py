def max_classify(class_matches, class_captures, class_capture_scores, negative_label="None"):
    return max(class_capture_scores, key=int) if class_capture_scores else negative_label
