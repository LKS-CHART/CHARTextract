from classifier.simple_capture_classifier import CaptureClassifier
from datahandler import data_import as di
from stats.basic import calculate_accuracy
from web.report_generator import generate_error_report
from web.report_generator import generate_classification_report
import os

if __name__ == "__main__":

    debug = True

    #Reading regex files
    regexes = {}

    #Importing immigration regexes
    filename = os.path.join("..","examples","regexes","tb_regexes", "immigration_country.txt")
    _, _, class_name, regexes[class_name] = di.regexes_from_csv(filename, use_custom_score=True, all_matches=False)

    if not debug:
        #Location of TB_DATA_FOLDER
        print("Current data folder: {!r}\n".format(os.getenv('TB_DATA_FOLDER')))

        #Label files and data files
        data_filenames = [os.path.normpath(os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Cohort 2 (really cleansed).csv'))]
        label_filenames = [os.path.normpath(os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Manual Chart Extraction - Cohort 2.xlsx'))]
        print("Files of interest: {!r}\n".format(data_filenames))
        print("Files of interest: {!r}\n".format(label_filenames))

        #Reading label data and importing data
        data, _, ids = di.data_from_csv(data_filenames, data_cols=2, id_cols=0, repeat_ids=False)
        _, temp_labels, temp_ids = di.data_from_excel(label_filenames, id_cols=1, label_cols=7, repeat_ids=False, first_row=2, check_col=1)
        labels = ["None"] * len(data)
        count = 0
        for i, data_id in enumerate(ids):
            if data_id in temp_ids:
                labels[i] = temp_labels[temp_ids.index(data_id)]
            else:
                count += 1

    else:
        data = ["She migrated from Trinidad in 1999", "He immigrated from the US in 1920. He moved to Canada in 1920", "He is Canadian."]
        labels = ["Trinidad", "US", "Canada"]
        ids = ["0", "1", "2"]


    #Dummy pwds
    pwds = {"country": ["Canada", "US", "Trinidad", "Nigeria"], "ethnicity": ["Canadian", "American", "Trinidadian", "Nigerian"]}

    #Convert ethnicities to country namse
    ethnicity_to_country = {ethnicity: country for country,ethnicity in zip(pwds["country"],pwds["ethnicity"])}
    def capture_convert(capture):
        if capture in ethnicity_to_country:
            return ethnicity_to_country[capture]

        return capture

    #Creating Naive Regex Classifier
    tb_regex_naive = CaptureClassifier("Basic Immigration Classifier", regexes)
    tb_regex_naive.import_data(data, labels, ids)
    tb_regex_naive.create_train_and_valid(0.6, 0)
    import time
    start = time.time()
    tb_regex_naive.run_classifier(sets=["train", "valid"], label_func=capture_convert, pwds=pwds)
    end = time.time()

    print("Total time:", end-start)

    #Calculating logistics for tb_regex_naive and generating templates
    for data_set in ["train", "valid"]:
        print("\n\nDataset:", data_set)
        #dataset accuarcy
        accuracy, incorrect_indices = calculate_accuracy(tb_regex_naive.dataset[data_set]["preds"],
                                                         tb_regex_naive.dataset[data_set]["labels"])

        print("\nPredictions:", tb_regex_naive.dataset[data_set]["preds"])
        print("\nLabels:", tb_regex_naive.dataset[data_set]["labels"])
        print("\nIds:", tb_regex_naive.dataset[data_set]["ids"])

        print("\nIncorrect Indices:", incorrect_indices)
        print("Incorrect Predictions: ", tb_regex_naive.dataset[data_set]["preds"][incorrect_indices])
        print("Actual Labels: ", tb_regex_naive.dataset[data_set]["labels"][incorrect_indices])
        print("Incorrect Ids:", tb_regex_naive.dataset[data_set]["ids"][incorrect_indices])

        print("\nAccuracy:", accuracy)

        failures_dict = {}
        all_patients_dict = {}

        for index in incorrect_indices:
            patient_id = tb_regex_naive.dataset[data_set]["ids"][index]
            pred = tb_regex_naive.dataset[data_set]["preds"][index]
            label = tb_regex_naive.dataset[data_set]["labels"][index]
            match_obj = tb_regex_naive.dataset[data_set]["matches"][index]
            score = tb_regex_naive.dataset[data_set]["scores"][index]
            data = tb_regex_naive.dataset[data_set]["data"][index]

            failures_dict[patient_id] = {"label": label, "data": data, "pred": pred, "matches": match_obj, "score": score}

        for index in range(len(tb_regex_naive.dataset[data_set]["ids"])):
            patient_id = tb_regex_naive.dataset[data_set]["ids"][index]
            pred = tb_regex_naive.dataset[data_set]["preds"][index]
            label = tb_regex_naive.dataset[data_set]["labels"][index]
            match_obj = tb_regex_naive.dataset[data_set]["matches"][index]
            score = tb_regex_naive.dataset[data_set]["scores"][index]
            data = tb_regex_naive.dataset[data_set]["data"][index]

            all_patients_dict[patient_id] = {"label": label, "data": data, "pred": pred, "matches": match_obj, "score": score}
