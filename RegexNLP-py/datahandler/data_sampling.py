import numpy as np


def create_train_and_valid(ids, data, labels, train_percent=.6, randomizer=None):
    """Splits data in train and valid

    Keyword Arguments:
        train_percent {float} -- Ratio of train/total (default: {.6})
        randomizer {np.random.RandomState} -- RandomState (default: {None})

    Returns:
        train ids{list} -- List of train ids
        valid ids{list} -- List of valid ids
    """

    if randomizer is None:
        randomizer = np.random.RandomState()

    x = randomizer.permutation(len(data))
    train = np.sort(x[:int(len(x) * train_percent)])
    valid = np.sort(x[int(len(x) * train_percent):])

    dataset = {"train": {}, "valid": {}}

    dataset["train"]["data"] = data[train]
    dataset["train"]["labels"] = labels[train]
    dataset["train"]["ids"] = ids[train]

    dataset["valid"]["data"] = data[valid]
    dataset["valid"]["labels"] = labels[valid]
    dataset["valid"]["ids"] = ids[valid]

    return dataset["train"], dataset["valid"]


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

    n_sample_data = []
    for i in range(n):
        cur_data = {"train": {"ids": [], "data": [], "labels": []}, "valid": {"ids": [], "data": [], "labels": []}}
        cur_data["train"], cur_data["valid"]["ids"] = \
            create_train_and_valid(ids, data, labels, train_percent, randomizer)

        n_sample_data.append(cur_data)
    return n_sample_data
