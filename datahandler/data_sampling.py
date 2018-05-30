import numpy as np


def n_cross_validation_samples(ids, data, labels, n, train_percent=.6, train_num=None, random_seed=None):
    if train_num is not None:
        if train_num <= len(ids):
            train_percent = train_num/len(ids)
        else:
            train_percent = 1

    if random_seed is not None:
        randomizer = np.random.RandomState(random_seed)
    else:
        randomizer = np.random.RandomState()

    x = randomizer.permutation(len(data))
    n_sample_data = []
    for i in range(n):
        cur_data = {"train": {"ids": [], "data": [], "labels": []}, "valid": {"ids": [], "data": [], "labels": []}}
        train = np.sort(x[:int(len(x) * train_percent)])
        valid = np.sort(x[int(len(x) * train_percent):])
        cur_data["train"]["data"] = data[train]
        cur_data["train"]["labels"] = labels[train]
        cur_data["train"]["ids"] = ids[train]

        cur_data["valid"]["data"] = data[valid]
        cur_data["valid"]["labels"] = labels[valid]
        cur_data["valid"]["ids"] = ids[valid]

        n_sample_data.append(cur_data)
    return n_sample_data
