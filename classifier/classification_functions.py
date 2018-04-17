def max_classify(class_matches, class_captures, class_capture_scores, negative_label="None"):
    return max(class_capture_scores, key=int) if class_capture_scores else negative_label

def min_classify(class_matches, class_captures, class_capture_scores, negative_label="None"):
    return min(class_capture_scores, key=int) if class_capture_scores else negative_label

def sputum_classify(class_matches, class_captures, class_capture_scores, negative_label="None"):
    sputum_matches = class_matches["Sputum conversion"]
    date_matches = class_matches["Sputum Date"]

    for case_index, case_matches in enumerate(sputum_matches):
        case_matches_values = case_matches.values()
        print(case_match_values)
        for matches in case_matches_values["matches"]:
            if matches["name"] == "reg0-Sputum conversion":
                print("MATCHY MATCHY")
                return negative_label


