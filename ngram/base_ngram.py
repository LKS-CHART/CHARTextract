from util.string_functions import split_string_into_sentences, split_string_into_words

class Ngram(object):
    def __init__(self, text, n, normalize_frequency=False, distance_weighting=False):
        self.text = text
        self.n = n
        self.ngram_to_frequency = {}
        self.ngram_to_matches = {}
        self._normalize_frequency = normalize_frequency
        self._distance_weighting = distance_weighting
        self.words = split_string_into_words(self.text)
        self.sentences = split_string_into_sentences(self.text)
        self._textlen = len(self.words)

    def top_k_ngrams(self, k):
        pass

    def remove_n_grams(self, ngrams):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __and__(self, other):
        pass

    def calculate_logistics(self):
        pass

    def _calculate_frequency(self):
        if self._distance_weighting:
            pass
        else:
            for i in range(self._textlen - self.n):
                ngram = " ".join(self.words[i:i+self.n])
                if ngram in self.ngram_to_frequency:
                    self.ngram_to_frequency[ngram] += 1
                else:
                    self.ngram_to_frequency = 1

        if self._normalize_frequency:
            num_ngrams = sum(self.ngram_to_frequency.values())
            self.ngram_to_frequency = {k: v/num_ngrams for k, v in self.ngram_to_frequency.items()}

    def _determine_match_locs(self):
        pass


class InvalidNgramOp(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
