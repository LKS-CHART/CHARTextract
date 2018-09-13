def get_unique_keys(main_ngram, other_ngram):
    '''
    Gets keys that appear in main_ngram but not in other_ngram

    :param main_ngram: Ngram you wish to compute the unique keys (Ngram)
    :param other_ngram: Ngram subtrahend (Ngram)

    :return: Dictionary of unique keys -> frequencies
    '''

    main_keys = set(main_ngram.ngram_to_frequency.keys()) - set(other_ngram.ngram_to_frequency.keys())
    return main_ngram.get_frequencies(list(main_keys))

def get_top_k(ngram_to_freq, k):
    '''
    Gets the top k frequency from an ngram->frequency dict

    :param ngram_to_freq: dictionary of ngram to frequency (str -> int)
    :param k: how many of the highest ngrams do you want to return (int)

    :return: Returns a list of sorted pairs of format (str, int)
    '''

    return sorted(ngram_to_freq.items(), key=lambda i: i[1], reverse=True)[:k]
