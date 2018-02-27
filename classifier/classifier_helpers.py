from regex.regex import Regex
from copy import copy

def get_matches_all_sentences(sentences, regexes):
    '''
    Given Regex objects and a list of sentences, computes all the matches

    :param sentences: A list of sentences (list of str)
    :param regexes: List of Regex Objects to search for in each sentence

    :return: {sentence_i: {"matches": [Regex Objects]}}
    '''
    matches_score_dict = {}

    for i, sentence in enumerate(sentences):
        matches = _get_sentence_matches(sentence, regexes)

        #only adding sentences that matched
        if matches:
            matches_score_dict[i] = {"matches": matches}

    return matches_score_dict

def _get_sentence_matches(sentence, regexes):
    '''
    Computes all matches in a sentence

    :param sentence: A string of text
    :param regexes: A list of Regex objects

    :return: List of Regex Objects that matched with the text
    '''

    matches = []
    for regex in regexes:

        #creating a copy because we want new unique regex objects for each match
        #reusing old regex objects will cause previous matches to be replaced by new matches and this behaviour
        #may not transfer well to multiple use cases

        regex_copy = copy(regex)
        regex_copy.clear_matches()

        #determining matches and computing score
        regex_matches = regex_copy.determine_matches(sentence)

        if len(regex_matches) > 0:
            #adding the new copied regex object to matches
            matches.append(regex_copy)

    return matches

