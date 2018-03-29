import numpy as np
def create_train_and_valid(data, train_percent=.6, random_seed=None):
    """Splits data in train and valid

    Keyword Arguments:
        train_percent {float} -- Ratio of train/total (default: {.6})
        random_seed {int} -- Seed for RandomState (default: {None})

    Returns:
        train ids{list} -- List of train ids
        valid ids{list} -- List of valid ids
    """
    if random_seed is not None:
        randomizer = np.random.RandomState(random_seed)
    else:
        randomizer = np.random.RandomState()

    x = randomizer.permutation(len(data))
    train = np.sort(x[:int(len(x) * train_percent)])
    valid = np.sort(x[int(len(x) * train_percent):])

    return data[train], data[valid], valid, train
