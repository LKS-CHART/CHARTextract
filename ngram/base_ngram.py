from util.string_functions import split_string_into_sentences, split_string_into_words
from copy import deepcopy

class Ngram(object):
    '''
    Ngram object which calculates ngram frequencies and matches from text.
    '''
    def __init__(self, text="", n=1, normalize_frequency=False, distance_weighting=False, freq_dict={}, match_dict={}):
        '''
        Initializes the Ngram object

        :param text: A string of text
        :param n: Ngram length e.g Unigram, Bigram, Tri etc.. (int)
        :param normalize_frequency: Normalize frequency values (bool)
        :param distance_weighting: Frequency calculation for an ngram takes into account the location of the match (bool)
        :param freq_dict: Pre-initialized ngram to frequency dict
        :param match_dict: Pre-initialized ngram to match dict
        '''

        self.text = text
        self.n = n
        self.ngram_to_frequency = freq_dict
        self.ngram_to_matches = match_dict
        self._normalize_frequency = normalize_frequency
        self._distance_weighting = distance_weighting
        self.words = split_string_into_words(self.text)
        self.sentences = split_string_into_sentences(self.text)
        self._textlen = len(self.words)

    def top_k_ngrams(self, k):
        '''
        Returns the k ngrams with highest frequency

        :param k: The number of ngrams you wish to return (int)

        :return: Returns a list of sorted pairs of format (ngram, frequency)
        '''

        return sorted(self.ngram_to_frequency.items(), key=lambda i: i[1], reverse=True)[:k]

    def remove_n_grams(self, ngrams):
        '''
        Removes the requested ngrams from ngram_to_frequency and ngram_to_matches dictionaries

        NOTE: This modified the Ngram Object

        :param ngrams: A list of ngrams (string) you wish to delete
        '''

        for ngram in ngrams:
            if ngram in self.ngram_to_frequency and self.ngram_to_matches:
                del self.ngram_to_frequency[ngram]
                del self.ngram_to_matches[ngram]

    def __add__(self, other):
        '''
        Adds the frequency dictionary of two Ngram objects of the same n

        TODO: Consider generic adding for Ngram objects (unlikely - too many ops are not well defined)

        :param other: Another ngram object

        :return: A new ngram to frequency dictionary which is the sum of the frequencies and keys
        '''

        if not isinstance(other, Ngram):
            raise InvalidNgramOp("Can only perform operations on Ngram Objects")

        if self.n != other.n:
            raise InvalidNgramOp("Ngrams must have the same n value")

        sum_ngram_dict = deepcopy(self.ngram_to_frequency)

        for ngram in other.ngram_to_frequency:
            if ngram in sum_ngram_dict:
                sum_ngram_dict[ngram] += other.ngram_to_frequency[ngram]
            else:
                sum_ngram_dict[ngram] = other.ngram_to_frequency[ngram]

        return sum_ngram_dict

    def __sub__(self, other):
        '''
        Subtract the frequency dictionary of two Ngram objects of the same n

        TODO: Consider generic subtraction for Ngram objects (unlikely - too many ops are not well defined)

        :param other: Another ngram object

        :return: A new ngram to frequency dictionary which is the difference of the frequencies
        '''

        if not isinstance(other, Ngram):
            raise InvalidNgramOp("Can only perform operations on Ngram Objects")

        if self.n != other.n:
            raise InvalidNgramOp("Ngrams must have the same n value")

        diff_ngram_dict = deepcopy(self.ngram_to_frequency)

        for ngram in other.ngram_to_frequency:
            if ngram in diff_ngram_dict:
                diff_ngram_dict[ngram] -= other.ngram_to_frequency[ngram]

        return diff_ngram_dict

    def __and__(self, other):
        '''
        Find the intersection of the frequency dictionary of two Ngram objects of the same n

        :param other: Another ngram object

        :return: A frequency dictionary which contains keys that only appear in both ngrams
        '''

        if not isinstance(other, Ngram):
            raise InvalidNgramOp("Can only perform operations on Ngram Objects")

        if self.n != other.n:
            raise InvalidNgramOp("Ngrams must have the same n value")

        and_ngram_dict = deepcopy(self.ngram_to_frequency)

        for ngram in self.ngram_to_frequency:
            if ngram not in other.ngram_to_frequency:
                del and_ngram_dict[ngram]

        return and_ngram_dict


    def get_normalized_frequency(self):
        '''
        Returns the normalized frequency as a dictionary of ngram -> normalized_frequency

        :return: Returns a ngram->normalized_frequency dictionary
        '''
        num_ngrams = sum(self.ngram_to_frequency.values())
        return {k: v/num_ngrams for k, v in self.ngram_to_frequency.items()}

    def calculate_logistics(self):
        '''
        Computes the ngram_to_frequency dictionary and the ngram_to_matches dictionary
        '''
        if self._distance_weighting:
            pass
        else:
            for i in range(self._textlen - self.n):
                ngram = " ".join(self.words[i:i+self.n])
                if ngram in self.ngram_to_frequency:
                    self.ngram_to_frequency[ngram] += 1
                    self.ngram_to_matches[ngram].append(i)
                else:
                    self.ngram_to_frequency = 1
                    self.ngram_to_matches[ngram] = [i]

        if self._normalize_frequency:
            self.ngram_to_frequency = self.get_normalized_frequency()


class InvalidNgramOp(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
