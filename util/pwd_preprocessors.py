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
