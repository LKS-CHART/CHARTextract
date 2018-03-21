from util.string_functions import split_string_into_sentences
from itertools import product
from heapq import *
from collections import defaultdict

class CaptureHandler(object):
    #TODO: Only works with primary regexes not secondary. Add this functionality later... Should pretty much be identical
    def __init__(self):
        pass

    def score_and_capture_sentences(self, text, regexes, pwds=None, preprocess_func=None):
        '''
        Given regexes and text
        :param text: Text to be split into sentences
        :param regexes: List of Regex objects to search for in sentences

        :return: matches, captures, capture_scores
        '''

        sentences = split_string_into_sentences(text)
        matches_scores_dict = {}
        captures = {}
        capture_scores = defaultdict(int)

        for i, sentence in enumerate(sentences):
            matches, captures, score = self.score_and_capture_sentence(sentence, regexes, capture_scores)

            if matches:
                matches_scores_dict[i] = {"matches": matches, "text_score": score}

        return matches_scores_dict, captures, capture_scores

    def score_and_match_sentence(self, text, regexes, capture_scores, pwds=None, preprocess_func=None):
        matches = []
        total_score = []

        #preprocessed_pwds = preprocess_func(text)

        for regex in regexes:
            regex_matches, regex_captures = regex.determine_matches(text)
            primary_matches = {"name": regex.name, "score": regex.score, "effect": regex.effect, "matches": regex_matches, "secondary_matches": []}
            for capture in regex_captures:
                capture_scores[capture] += regex.score

            primary_matches["matches"].extend(regex_captures)


        return


class RegexHandler(object):

    def __init__(self):
        pass

    def _match_secondary(self, secondary_regex, text, primary_regex_matches):
        secondary_matches = secondary_regex.determine_matches(text)

        if secondary_matches:
            if len(secondary_regex.effect) == 2:
                effect_modifier = secondary_regex.effect[1]
                if effect_modifier == "b" and any(map(lambda tup: tup[0].start() < tup[1].start(), product(secondary_matches, primary_regex_matches))):
                    secondary_matches = secondary_matches
                elif effect_modifier == "a" and any(map(lambda tup: tup[0].start() > tup[1].end(), product(secondary_matches, primary_regex_matches))):
                    secondary_matches = secondary_matches
                else:
                    secondary_matches = []

        return secondary_matches

    def score_and_match_sentences(self, text, regexes):
        '''
        Given regexes and text, determines a score for the sentence

        :param text: Text to be split into sentences
        :param regexes: List of Regex Objects to search for in each sentence

        :return: {sentence_i: {'matches': [Match dicts], 'score': sentence_score}} and a total_score
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

        :return: List of Match dicts {"primary_name", "primary_score", "primary_effect", "primary_matches":[], "secondary_matches": [{"name","effect","score","matches"}]} that matched with the text, total_score
        '''

        matches = []
        total_score = 0
        for regex in regexes:
            regex_matches = regex.determine_matches(text)
            score = regex.score*len(regex_matches)
            priority_queue = []
            secondary_matches = []
            primary_match = {"name": regex.name, "score": regex.score, "effect": regex.effect, "matches": regex_matches, "pattern": regex.regex.pattern, "secondary_matches": []}

            if len(regex_matches) > 0:
                ignore_regexes = regex.get_secondary_regexes(type_list=["i", "ib", "ia"])
                replace_regexes = regex.get_secondary_regexes(type_list=["r", "rb", "ra"])
                add_regexes = regex.get_secondary_regexes(type_list=["a", "ab", "aa"])

                for i, secondary_regex in enumerate(ignore_regexes): heappush(priority_queue, (i, secondary_regex))
                for i, secondary_regex in enumerate(replace_regexes): heappush(priority_queue, (i+len(ignore_regexes), secondary_regex))
                for i, secondary_regex in enumerate(add_regexes): heappush(priority_queue, (i+len(ignore_regexes) + len(replace_regexes), secondary_regex))

                for i in range(len(priority_queue)):
                    secondary_regex = heappop(priority_queue)[1]
                    secondary_regex_obj = {"name": secondary_regex.name, "effect": secondary_regex.effect, "pattern": secondary_regex.regex.pattern, "score": secondary_regex.score, "matches": []}
                    secondary_match = self._match_secondary(secondary_regex, text, regex_matches)

                    if secondary_match:
                        secondary_regex_obj["matches"] = secondary_match
                        secondary_matches.append(secondary_regex_obj)

                        if secondary_regex.effect.startswith("i"):
                            score = 0
                            break

                        elif secondary_regex.effect.startswith("r"):
                            score = secondary_regex.score
                            break

                        elif secondary_regex.effect.startswith("a"):
                            score += secondary_regex.score

                primary_match["secondary_matches"] = secondary_matches
                matches.append(primary_match)

            total_score += score

        return matches, total_score
