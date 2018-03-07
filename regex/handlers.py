from util.string_functions import split_string_into_sentences
from copy import copy
from itertools import product
from heapq import *

class RegexHandler(object):

    def __init__(self):
        pass

    def score_and_match_sentences(self, text, regexes):
        '''
        Given regexes and text, determines a score for the sentence

        :param text: Text to be split into sentences
        :param regexes: List of Regex Objects to search for in each sentence

        :return: {sentence_i: {'matches': [Regex Objects], 'score': sentence_score}} and a total_score
        '''

        sentences = split_string_into_sentences(text)
        matches_score_dict = {}
        total_score = 0

        for i, sentence in enumerate(sentences):
            matches, score = self.score_and_match_sentence(sentence, regexes)

            #only adding sentences that matched
            if matches:
                matches_score_dict[i] = {"matches": matches, "text_score": score}

            total_score += score

        return matches_score_dict, total_score

    def score_and_match_sentence(self, text, regexes):
        '''
        Scores the text and returns matches based on the effects of the regexes

        :param text: A string of text
        :param regexes: A list of Regex objects

        :return: List of Regex Objects that matched with the text, total_score
        '''

        matches = []
        total_score = 0
        for regex in regexes:

            #creating a copy because we want new unique regex objects for each match
            #reusing old regex objects will cause previous matches to be replaced by new matches and this behaviour
            #may not transfer well to multiple use cases

            regex_copy = copy(regex)
            regex_copy.clear_matches()

            #determining matches and computing score
            regex_matches = regex_copy.determine_matches(text)
            score = regex.score*len(regex_matches)
            should_add_regex = True

            #TODO: Lots of duplicated code here. Fix this later

            if len(regex_matches) > 0:
                #adding the new copied regex object to matches
                ignore_matches = regex_copy.determine_secondary_matches(text, ["i", "ib", "ia"])
                ignore_matched = True if ignore_matches else False

                if ignore_matched:
                    for i in range(len(ignore_matches)):
                        ignore_matched = False
                        _, effect, matches, _ = heappop(ignore_matches)

                        if effect == "i":
                            ignore_matched = True
                        elif effect == "ib" and any(map(lambda match_ignore, match_primary: match_ignore.start() < match_primary.start(),
                                                        product(matches, regex_matches))):
                            ignore_matched = True

                        elif effect == "ia" and any(map(lambda match_ignore, match_primary: match_ignore.start() > match_primary.end(),
                                                        product(matches, regex_matches))):
                            ignore_matched = True

                        if ignore_matched:
                            score = 0
                            should_add_regex = False
                            break

                if not ignore_matched:
                    replace_matches = regex_copy.determine_secondary_matches(text, ["r", "rb", "ra"])
                    replace_matched = True if replace_matches else False

                    if replace_matched:
                        for i in range(len(replace_matches)):
                            replace_matched = False
                            _, effect, matches, rscore = heappop(replace_matches)

                            if effect == "r":
                                replace_matched = True
                            elif effect == "rb" and any(map(lambda match_replace, match_primary: match_replace.start() < match_primary.start(),
                                                            product(matches, regex_matches))):
                                replace_matched = True

                            elif effect == "ra" and any(map(lambda match_replace, match_primary: match_replace.start() > match_primary.end(),
                                                            product(matches, regex_matches))):
                                replace_matched = True

                            if replace_matched:
                                score = rscore
                                break

                    if not replace_matched:
                        add_matches = regex_copy.determine_matches(text, ["a", "ab", "aa"])

                        for i in range(len(add_matches)):
                            _, effect, matches, rscore = heappop(add_matches)

                            if effect == "a":
                                total_score += rscore
                            elif effect == "ab" and any(map(lambda match_replace, match_primary: match_replace.start() < match_primary.start(),
                                                            product(matches, regex_matches))):
                                total_score += rscore

                            elif effect == "aa" and any(map(lambda match_replace, match_primary: match_replace.start() > match_primary.end(),
                                                            product(matches, regex_matches))):
                                total_score += rscore

                if should_add_regex:
                    matches.append(regex_copy)

            total_score += score

        return matches, total_score

