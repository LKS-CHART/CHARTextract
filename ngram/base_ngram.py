class Ngram(object):
    def __init__(self, text, n):
        self.text = text
        self.n = n
        self._textlen = None
        self.ngram_to_frequency = None
        self.ngram_to_matches = None

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
        pass

    def _determine_match_locs(self):
        pass

    def _split_string(self):
        pass


class InvalidNgramOp(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
