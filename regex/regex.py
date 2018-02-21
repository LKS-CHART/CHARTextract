import re

class Regex(object):
    '''
    Container class for regexes, scores and matches
    '''
    def __init__(self, name="Regex", regex=None, score=None):
        self.name = name
        self.regex = re.compile(regex)
        self.score = score
        self.matches = None

    def __str__(self):
        '''
        Returns stringified dict of Regex object parameters and values

        :return: Dictionary of regex_params->values
        '''

        return str({"name": self.name, "regex": self.regex.pattern, "score": self.score, "matches": self.matches})

    def __repr__(self):
        '''
        Returns object representation of Regex object parameters and values

        TODO: Differentiate this from __str__ somehow

        :return: Dictionary of regex_params->values
        '''

        return repr({"name": self.name, "regex": self.regex, "score": self.score, "matches": self.matches})
