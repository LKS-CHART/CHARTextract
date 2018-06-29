from datahandler import data_sampling
from regex.handlers import RegexHandler


def matched_regexes(ids, data, regexes, pwds, preprocess_func):
    found_regexes = []
    handler = RegexHandler(return_ignores=True)
    for single_regex in regexes:
        for i in range(len(ids)):
            matches, total_score = handler.score_and_match_sentences(data[i], [single_regex], pwds, preprocess_func)
            print(matches)
            exit()
    return found_regexes


def n_cross(ids, data, labels, n, regexes, pwds, preprocess_func, train_percent=.6, train_num=None, random_seed=None):
    n_samples = data_sampling.n_cross_validation_samples(ids, data, labels, n, train_percent, train_num, random_seed)
    n_regexes = []
    for each in n_samples:
        n_regexes.append(matched_regexes(each["ids"], each["data"], regexes, pwds, preprocess_func))

    return n_regexes, n_samples


def rank_ids(n_samples, n_regexes):
    id_ranks = {}
    for sample in n_samples:
        for i in range(len(sample["ids"])):
            num_matches = 0
            for regexes in n_regexes:
                if regexes.