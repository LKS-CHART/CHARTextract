import re
from regex.regex_functions import combine_flags

class Regex(object):
    """Container class for regexes, scores and matches
    """

    def __init__(self, name, regex, effect, score, secondary_regexes=None, all_matches=False, flags=None):
        """Initialize Regex object
        
        Arguments:
            name {String} -- Regex name
            regex {String} -- Regular expression
            effect {String} -- Effect e.g "rb"
            score {int} -- Regex score
        
        Keyword Arguments:
            secondary_regexes {list} -- List of secondary Regex objects (default: {None})
            all_matches {bool} -- Return first match or all matches (default: {False})
            flags {list} -- List of regex flags to be used for compilation e.g [re.IGNORECASE, re.DEBUG] (default: {None})
        """

        self.name = name
        self.score = score
        self.all_matches = all_matches
        self.effect = effect
        self._match_func = re.finditer if all_matches else re.search
        self.matches = None
        self._should_compile = regex.find("dict:'") == -1 #Don't compile if it found dict:'
        # self._should_compile = False
        self.flags = combine_flags(flags) if flags else 0
        self.regex = re.compile(regex, self.flags) if self._should_compile else regex
        self._required_pwds = [] if self._should_compile else self._get_required_pwds()
        self.secondary_regexes = tuple(secondary_regexes)

    def get_regex(self):
        """Return the regex pattern
        
        Returns:
            regex {String} -- Regex pattern
        """

        return self.regex.pattern if self._should_compile else self.regex

    def _add_dict_to_pattern(self, regex, required_pwds, pwds):
        """Inserts the required dictionary lists into the pattern. E.g "(He|She) is from {country}" -> country_list
        
        Arguments:
            regex {String} -- Regex
            required_pwds {list} -- List of required pwds
            pwds {dict} -- Personalized word dictionary {"dict_name" -> list}
        
        Returns:
            regex {String} -- Modified regex with dictionary inserted
        """

        #string.format can't work if we regexes which have curly braces like so \d{4} since str.format expects a value
        #opting for a simple replace method

        regex_pwds = {key: "|".join(pwds[key]) for key in required_pwds}

        for key in regex_pwds:
            regex = regex.replace("{{{}}}".format(key), regex_pwds[key])

        return regex



    def _get_required_pwds(self):
        """Removes dict:\(dictionary_name\) from the regex and replaces it with {dictionary_name}. Also returns the dictionaries that are required by the
        regex
        
        Returns:
            Required Pwds {list} -- List of required pwds
        """

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
        """Sets the type of match function used by the regex
        
        Arguments:
            all_matches {bool} -- If all_matches is True, returns all the matches in the text
        
        Returns:
            all_matches {bool} -- Returns all_matches state
        """

        '''
        Set the all_matches parameter in Regex object

        :param all_matches: if True, determine_matches will return all matches else just the first one

        :return: self.all_matches (bool)
        '''

        self.all_matches = all_matches
        self._match_func = re.finditer if all_matches else re.search

        return self.all_matches

    def __str__(self):
        """Returns stringified dict of Regex object parameters and values
        
        Returns:
            String -- Stringified version of Regex object
        """
        return str({"name": self.name, "regex": self.regex.pattern, "score": self.score, "matches": self.matches, "secondary_regexes": self.secondary_regexes})

    def __repr__(self):

        """Returns stringified dict of Regex object parameters and values
        
        Returns:
            String -- Repr of Regex object
        """

        return repr({"name": self.name, "regex": self.regex, "score": self.score, "matches": self.matches, "secondary_regexes": self.secondary_regexes})

    #TODO: Temporary placeholder method. Transfer functionality into determine_matches (Maybe)
    def determine_captures_w_matches(self, text, pwds=None):
        """Compute the matches and captures for a given text
        
        Arguments:
            text {String} -- Text
        
        Keyword Arguments:
            pwds {dict} -- Personalized word dictionary (default: {None})
        
        Returns:
            matches {list} -- List of MatchObjects
            captures {list} -- List of captured strings
        """

        if pwds:
            regex = self._add_dict_to_pattern(self.regex, self._required_pwds, pwds)
            print(regex)

        #Want to keep format for re.iter and re.search the same so that's why I'm returning lists
        if self.all_matches:
            #Use re.iter if all matches and return a list version
            matches = list(self._match_func(self.regex, text)) if self._should_compile else self._match_func(regex, text, self.flags)
        else:
            #Use re.search if not and return a list version
            matches = self._match_func(self.regex, text) if self._should_compile else self._match_func(regex, text, self.flags)
            matches = [] if matches is None else [matches]

        captures = [capture for match in matches for capture in match.groups()]

        return matches, captures

    def determine_matches(self, text, pwds=None):

        """Compute the matches a given text
        
        Arguments:
            text {String} -- Text
        
        Keyword Arguments:
            pwds {dict} -- Personalized word dictionary (default: {None})
        
        Returns:
            matches {list} -- List of MatchObjects
        """

        if pwds:
            regex = self._add_dict_to_pattern(self.regex, self._required_pwds, pwds)

        if self.all_matches:
            #Use re.iter if all matches and return a list version
            matches = list(self._match_func(self.regex, text)) if self._should_compile else self._match_func(regex, text, self.flags)
        else:
            #Use re.search if not and return a list version
            matches = self._match_func(self.regex, text) if self._should_compile else self._match_func(regex, text, self.flags)
            matches = [] if matches is None else [matches]

        return matches

    def get_secondary_regexes(self, type_list=None):
        """Returns a list of secondary regexes with the given effect type. If type_list is None return all
        
        Keyword Arguments:
            type_list {list} -- List of regex effects (default: {None})
        
        Returns:
            secondary_regexes {tuple} -- List of secondary regexes with the given effect
        """

        secondary_regexes = []

        for secondary_regex in self.secondary_regexes:
            if secondary_regex.effect in type_list or not type_list:
                secondary_regexes.append(secondary_regex)

        return tuple(secondary_regexes)

