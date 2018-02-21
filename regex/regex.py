import re
from regex.regex_functions import combine_flags

class Regex(object):
    '''
    Container class for regexes, scores and matches
    '''
    def __init__(self, name, regex, score, all_matches=False, flags=None):
        '''
        Initialize Regex object

        :param name: Regex name (string)
        :param regex: Regular expression (string)
        :param score: Regex score (int)
        :param all_matches: Return first match or all matches (bool)
        :param flags: list of regex flags to be used for compilation e.g [re.IGNORECASE, re.DEBUG]
        '''

        self.name = name
        self.score = score
        self.all_matches = all_matches
        self._match_func = re.finditer if all_matches else re.search
        self.matches = None

        if flags is None:
            self.regex = re.compile(regex)
        else:
            self.regex = re.compile(regex, combine_flags(flags))

    def set_match_all(self, all_matches):
        '''
        Set the all_matches parameter in Regex object

        :param all_matches: if True, determine_matches will return all matches else just the first one

        :return: self.all_matches (bool)
        '''

        self.all_matches = all_matches
        self._match_func = re.finditer if all_matches else re.search

        return self.all_matches

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

    def determine_matches(self, text):
        '''
        Compute the matches for a given text

        :param text: A string of text for which you want to find matches for

        :return: A list containing one MatchObject or multiple depending on all_matches parameter
        '''

        if self.all_matches:
            self.matches = list(self._match_func(self.regex, text))
        else:
            self.matches = self._match_func(self.regex, text)




