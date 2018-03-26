import re
from regex.regex_functions import combine_flags
from heapq import *
from copy import copy

class Default(dict):
    def __missing__(self, k): return '{' + k + '}'

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
        self._should_compile = regex.find("dict:'") == -1 #Don't compile if it found dict:'
        self.flags = combine_flags(flags) if flags else 0
        self.regex = re.compile(regex, self.flags) if self._should_compile else regex
        self._required_pwds = [] if self._should_compile else self._get_required_pwds()
        self.secondary_regexes = tuple(secondary_regexes)

    def get_regex(self):
        return self.regex.pattern if self._should_compile else self.regex

    def _add_dict_to_pattern(self, regex, required_pwds, pwds):
        #string.format can't work if we regexes which have curly braces like so \d{4} since str.format expects a value
        #opting for a simple replace method

        regex_pwds = {key: "|".join(pwds[key]) for key in required_pwds}

        for key in regex_pwds:
            regex = regex.replace("{{{}}}".format(key), regex_pwds[key])

        return regex



    def _get_required_pwds(self):
        pwds = []

        def replace_pattern(match_obj):
            pwds.append((match_obj.group(2)))
            if match_obj.group(1) == "\(":
                return "({{{}}})".format(match_obj.group(2))
            else:
                return "{{{}}}".format(match_obj.group(2))

        check_pattern = r"{}(\\\()?([^\s)]+)(\\\))?{}".format("dict:'", "'")
        self.regex, n = re.subn(check_pattern, replace_pattern, self.regex)

        return list(set(pwds))


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

    #TODO: Temporary placeholder method. Transfer functionality into determine_matches (Maybe)
    def determine_captures_w_matches(self, text, pwds=None):
        '''
        Computer the matches and captures for a given text
        '''

        if pwds:
            regex = self._add_dict_to_pattern(self.regex, self._required_pwds, pwds)

        #maybe pass in arg list instead of repeating self._match_func calls.. honestly I'm just being picky now
        if self.all_matches:
            matches = list(self._match_func(regex, text)) if self._should_compile else self._match_func(regex, text, self.flags)
        else:
            matches = self._match_func(regex, text) if self._should_compile else self._match_func(regex, text, self.flags)
            matches = [] if matches is None else [matches]

        captures = [capture for match in matches for capture in match.groups()]

        return matches, captures

    def determine_matches(self, text, pwds=None):
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

