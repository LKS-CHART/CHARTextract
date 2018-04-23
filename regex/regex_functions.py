import functools
import operator
from itertools import product

def combine_flags(flag_list):
    """Combines regex flags using bitwise or
    
    Arguments:
        flag_list {list} -- List of flags e.g [re.IGNORECASE, re.DEBUG]
    
    Returns:
        int -- Bitwise or of flags
    """

    #Or operator applied to flag_list
    return functools.reduce(operator.or_, flag_list)

# TODO: Maybe create an effect handler
def _match_secondary(self, secondary_regex, text, primary_regex_matches, pwds=None):
    """Computes matches for the secondary regex

    Arguments:
        secondary_regex {Regex} -- Secondary Regex object to compute the matches for
        text {String} -- Text to match
        primary_regex_matches {list} -- List of MatchObjs for primary regex

    Returns:
        secondary_matches {list} -- List of MatchObjs for secondary regex
    """

    # Getting secondary matches
    secondary_matches = secondary_regex.determine_matches(text, pwds=pwds)
    if self.DEBUG:
        print("SECONDARY_MATCHES IN FUNC:", secondary_matches)

    if secondary_matches:
        # If regex has a before or after effect e.g rb, ia etc.. do some extra checks based on effect
        # Otherwise, just return secondary_matches
        if len(secondary_regex.effect) == 2:
            effect_modifier = secondary_regex.effect[1]
            # If secondary match appears before any of the primary matches
            if effect_modifier == "b" and any(map(lambda tup: tup[0].start() <= tup[1].start(),
                                                  product(secondary_matches, primary_regex_matches))):
                secondary_matches = secondary_matches
            # If it appears after any of the primary matches
            elif effect_modifier == "a" and any(map(lambda tup: tup[0].start() >= tup[1].end(),
                                                    product(secondary_matches, primary_regex_matches))):
                secondary_matches = secondary_matches

            # If the above two were not satisfied, the secondary regex failed to satisfy its after effect
            else:
                secondary_matches = []

    return secondary_matches
