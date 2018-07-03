from util.string_functions import split_string_into_words
import copy

class PwdPreprocessor:
    def __init__(self, pwds, categories_of_interest):
        self.pwds = pwds
        self.categories = categories_of_interest

    def preprocess(self, text, *args):
        output_dictionary = {"sentence": text, "dictionaries": {}}
        keep_data = False

        for category in self.categories:
            output_dictionary["dictionaries"][category] = []
            for term in self.pwds[category]:
                if term in text:
                    output_dictionary["dictionaries"][category].append(term)
                    keep_data = True

        if keep_data:
            return output_dictionary
        else:
            return {"sentence": None, "dictionaries": None}

class PwdPreprocessor2:
    def __init__(self, pwds, categories_of_interest, to_lower=False):
        self.pwds = pwds
        self.categories = categories_of_interest
        self.to_lower = to_lower

        if self.to_lower:
            self.pwds = {category: {term.lower() for term in self.pwds[category]}
                         for category in categories_of_interest}
        else:
            self.pwds = {category: {term for term in self.pwds[category]}
                         for category in categories_of_interest}

    def _create_ngram(self, text, k=1, to_lower=False):
        text_tokens = split_string_into_words(text)
        ngrams = []

        for i in range(len(text_tokens) - k):
            ngram = " ".join(text_tokens[i:i+k]).lower() if to_lower else " ".join(text_tokens[i:i+k])
            ngrams.append(ngram)

        return ngrams

    def preprocess(self, text, *args):
        output_dictionary = {"sentence": text, "dictionaries": {}}

        required_categories = tuple(self.categories)

        if len(args) >= 1:
            required_categories = tuple(args)

        matches = [False]*len(required_categories)

        for j, category in enumerate(required_categories):
            output_dictionary["dictionaries"][category] = []

            ngrams = {i: self._create_ngram(text, k=i, to_lower=self.to_lower) for i in range(1,4,1)}

            for ngram in ngrams:
                for term in ngrams[ngram]:
                    if term in self.pwds[category]:
                        output_dictionary["dictionaries"][category].append(term)
                        matches[j] = True

        keep_data = any(matches)

        if keep_data:
            return output_dictionary
        else:
            return {"sentence": None, "dictionaries": None}



