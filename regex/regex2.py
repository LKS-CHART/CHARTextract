import re
from regex.regex_functions import combine_flags
from heapq import *
from copy import copy

class Regex(object):
    '''
    Container class for regexes, scores and matches
    '''
    def __init__(self, name, regex, effect, score, secondary_regexes=None, all_matches=False, flags=None):
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
        self.effect = effect
        self._match_func = re.finditer if all_matches else re.search
        self.matches = None

        if flags is None:
            self.regex = re.compile(regex)
        else:
            self.regex = re.compile(regex, combine_flags(flags))

        self.secondary_regexes = tuple(secondary_regexes)

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

        return str({"name": self.name, "regex": self.regex.pattern, "score": self.score, "matches": self.matches, "secondary_regexes": self.secondary_regexes})

    def __repr__(self):
        '''
        Returns object representation of Regex object parameters and values

        :return: Dictionary of regex_params->values
        '''

        return repr({"name": self.name, "regex": self.regex, "score": self.score, "matches": self.matches, "secondary_regexes": self.secondary_regexes})

    def clear_matches(self):
        self.matches = None

    #TODO: Temporary placeholder method. Transfer functionality into determine_matches
    def determine_captures_w_matches(self, text):
        '''
        Computer the matches and captures for a given text
        '''

        if self.all_matches:
            matches = list(self._match_func(self.regex, text))
        else:
            matches = self._match_func(self.regex, text)
            matches = [] if matches is None else [matches]

        captures = [capture for match in matches for capture in match.groups()]
        print(matches)
        print(captures)

        return matches, captures

    def determine_matches(self, text):
        '''
        Compute the matches for a given text

        :param text: A string of text for which you want to find matches for

        :return: A list containing one MatchObject or multiple depending on all_matches parameter
        '''

        if self.all_matches:
            matches = list(self._match_func(self.regex, text))

        else:
            matches = self._match_func(self.regex, text)
            matches = [] if matches is None else [matches]

        return matches

    def get_secondary_regexes(self, type_list=None):
        secondary_regexes = []

        for secondary_regex in self.secondary_regexes:
            if secondary_regex.effect in type_list or not type_list:
                secondary_regexes.append(secondary_regex)

        return tuple(secondary_regexes)

