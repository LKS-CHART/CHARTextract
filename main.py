from variable_classifiers.base_runner import Runner, import_regexes
from datahandler import data_import as di
import os

if __name__ == "__main__":
    data_filenames = [os.path.normpath(os.path.join(os.getenv('TB_DATA_FOLDER'), 'NLP Study (TB Clinic) Cohort 2 (really cleansed).csv'))]
    data, _, ids = di.data_from_csv(data_filenames, data_cols=2, id_cols=0, repeat_ids=False)
    regex_dir = os.path.join('examples', 'regexes', 'tb_regexes', 'smoking_new')

    regexes = import_regexes(regex_dir)
    regex_biases = {regex_name: (0 if regex_name is not "None" else 1) for regex_name in regexes}

    smoking_classifier_args = {"classifier_name": "Smoking Classifier", "regexes": regexes, "biases": regex_biases}
    smoking_classifier = Runner("RegexClassifier", **smoking_classifier_args)

    smoking_classifier.run(ids=ids, data=data)

    print(smoking_classifier.classifier.dataset["test"]["preds"])
