from util.string_functions import split_string_into_sentences
from itertools import product
from heapq import *
from collections import defaultdict
from regex.regex_functions import match_secondary

PREPROCESS_BEFORE_REGEXES = 1
PREPROCESS_PER_REGEX = 2

class TextCaptureHandler(object):

    def __init__(self):
        self.DEBUG = False
        pass


class CaptureHandler(object):
    # TODO: Only works with primary regexes not secondary. Add this functionality later... Should pretty much be identical
    # TODO: Add generic score_and_capture_text and have score_and_capture_sentence call that

    """Used for capturing and scoring sentences. Can be used by CaptureClassifier
    """

    def __init__(self, return_ignores=False, preprocess_mode=PREPROCESS_PER_REGEX):
        self.DEBUG = False
        self.return_ignores = return_ignores
        self.preprocess_mode = preprocess_mode
        pass

    def score_data(self, text, regexes, pwds=None, preprocess_func=None, capture_convert=None):
        matches_scores_dict, captures, capture_scores = self.score_and_capture_sentences(text, regexes, pwds=pwds,
                                                                                         preprocess_func=preprocess_func,
                                                                                         capture_convert=capture_convert)

        return matches_scores_dict, captures, capture_scores

    def score_and_capture_sentences(self, text, regexes, pwds=None, preprocess_func=None, capture_convert=None):
        """Given regexes and text, returns the matches, captures
        
        Arguments:
            text {String} -- Text to be split into sentences
            regexes {list} -- List of Regex objects to search for in sentences
        
        Keyword Arguments:
            pwds {dict} -- Dictionary of dict_name -> list of words (default: {None})
            preprocess_func {function} -- Function to preprocess sentences and pwds (default: {None})
            capture_convert {function} -- Function that converts the capture to a label (i.e some mapping function) (default: {None})
        
        Returns:
            matches {dict} -- {sentence_i -> {"matches" -> list of modified match obj, "text_score": score (for sentence)}}
            captures {list} -- list of captured text
            capture_scores {dict} -- {"captured_text" -> score}
        """
        sentences = split_string_into_sentences(text)
        matches_scores_dict = {}
        captures_list = []
        capture_scores = defaultdict(int)

        # Scoring and capturing each sentence
        for i, sentence in enumerate(sentences):
            if sentence == '':
                continue

            # Mimicing preprocessing from old tool
            sentence = " {} ".format(sentence)

            preprocessed_data = {}

            # Preprocessing sentence
            if preprocess_func and self.preprocess_mode==PREPROCESS_BEFORE_REGEXES:
                preprocessed_data = preprocess_func(sentence)
            else:
                preprocessed_data["sentence"] = sentence
                preprocessed_data["dictionaries"] = pwds

            if preprocessed_data["sentence"] is None:
                continue

            matches, captures, score = self.score_and_capture_sentence(preprocessed_data["sentence"], regexes,
                                                                       capture_scores,
                                                                       pwds=preprocessed_data["dictionaries"],
                                                                       capture_convert=capture_convert, preprocess_func=preprocess_func)

            if matches:
                matches_scores_dict[i] = {"matches": matches, "text_score": score}

            # TODO: Decide on whether to do sentence_number -> capture for captures or just append all captures to a list
            # if captures:
            #    captures_dict[i] = {"captures": captures}

            captures_list.extend(captures)

        if self.DEBUG:
            print(capture_scores)

        return matches_scores_dict, captures_list, capture_scores

    def score_and_capture_sentence(self, text, regexes, capture_scores, pwds=None, capture_convert=None, preprocess_func=None):
        """Given regexes and text, returns the matches, captures
        
        Arguments:
            text {String} -- sentence
            regexes {list} -- List of Regex objects to search for in sentences
            capture_scores {dict} -- Dictionary which maps the captured text to a score
        
        Keyword Arguments:
            pwds {dict} -- Dictionary of dict_name -> list of words (default: {None})
            preprocess_func {function} -- Function to preprocess sentences and pwds (default: {None})
            capture_convert {function} -- Function that converts the capture to a label (i.e some mapping function) (default: {None})
        
        Returns:
            matches {dict} -- [List of modified match_objects] 
            captures {list} -- list of captured text
            score {int} -- sentence score
        """
        matches = []
        captures = []
        total_score = 0


        # For every regex we want to get the captures, matches and compute a score using the primary regex score
        for regex in regexes:

            preprocessed_data = {}
            if preprocess_func and self.preprocess_mode == PREPROCESS_PER_REGEX:
                secondaries = regex.get_secondary_regexes()
                mentioned_pwds = set({secondary._required_pwds for secondary in secondaries})
                mentioned_pwds = list(set(regex._required_pwds) | mentioned_pwds)
                preprocessed_data = preprocess_func(text, *mentioned_pwds)
            else:
                preprocessed_data["sentence"] = text
                preprocessed_data["dictionaries"] = pwds

            if preprocessed_data["sentence"] is None:
                continue

            # Getting matches and captures
            regex_matches, regex_captures = regex.determine_captures_w_matches(preprocessed_data["sentence"], pwds=preprocessed_data["dictionaries"])

            # If regex returns all the matches want to multiply score by length
            score = regex.score*len(regex_matches)

            # Converting the capture using the capture_convert function
            # E.g Canadian -> Canada, Trinidadian -> Trinidad

            # Creating priority for regex effects. Ignores have highest precedence followed by replaces and lastly adds
            priority_queue = []
            secondary_matches = []
            primary_match = {"name": regex.name, "score": regex.score, "effect": regex.effect, "matches": regex_matches, "pattern": regex.get_regex(), "secondary_matches": [], "aggregate_score": 0}
            add_primary_match = True

            # If the primary matches
            if len(regex_matches) > 0:

                # Getting all the secondary regexes grouped by effect
                ignore_regexes = regex.get_secondary_regexes(type_list=["i", "ib", "ia"])
                replace_regexes = regex.get_secondary_regexes(type_list=["r", "rb", "ra"])
                add_regexes = regex.get_secondary_regexes(type_list=["a", "ab", "aa"])

                # Pushing secondary regexes on to priority queue. Priority queue key is determined by order of appearance in secondary_regexes list and also their effect
                for i, secondary_regex in enumerate(ignore_regexes): heappush(priority_queue, (i, secondary_regex))
                for i, secondary_regex in enumerate(replace_regexes): heappush(priority_queue, (i+len(ignore_regexes), secondary_regex))
                for i, secondary_regex in enumerate(add_regexes): heappush(priority_queue, (i+len(ignore_regexes) + len(replace_regexes), secondary_regex))
                if self.DEBUG:
                    print("Regex: ", regex.get_regex())
                    print("TEXT: ", text)
                    print("Before filter:", regex_matches)
                    print("IGNORE REGEXES:", ignore_regexes)
                    print("REPLACE REGEXES:", replace_regexes)
                    print("ADD REGEXES:", add_regexes)
                    print("PRIORITY QUEUE:", priority_queue)

                for i in range(len(priority_queue)):
                    # Pop the secondary regex off the queue and compute the secondary matches
                    secondary_regex = heappop(priority_queue)[1]
                    secondary_regex_obj = {"name": secondary_regex.name, "effect": secondary_regex.effect, "pattern": secondary_regex.get_regex(), "score": secondary_regex.score, "matches": []}
                    secondary_match = match_secondary(secondary_regex, preprocessed_data["sentence"], regex_matches, pwds=preprocessed_data["dictionaries"])


                    # If there was a secondary match
                    if secondary_match:
                        if self.DEBUG:
                            print("After filter", regex_matches)
                            print("Secondary Match: ", secondary_match)
                        # Update secondary_regex_obj matches component
                        secondary_regex_obj["matches"] = secondary_match
                        # Add the secondary_regex_obj to the list of secondary_matches for the primary_regex_obj
                        secondary_matches.append(secondary_regex_obj)

                        # If ignore, stop eval of remaining secondary regexes
                        if secondary_regex.effect.startswith("i"):
                            score = 0
                            add_primary_match = self.return_ignores
                            break

                        # If replace, replace score and stop eval of remaining secondary regexes
                        elif secondary_regex.effect.startswith("r"):
                            score = secondary_regex.score

                        # If add, add to the score
                        elif secondary_regex.effect.startswith("a"):
                            score += secondary_regex.score

                    else:
                        if secondary_regex.effect.startswith("r"):
                            break

                # Setting primary regex's secondary matches param
                primary_match["secondary_matches"] = secondary_matches
                primary_match["aggregate_score"] = score

                # Add the primary regex to the list of matches for the sentence
                if add_primary_match:
                    matches.append(primary_match)
                    captures.extend(regex_captures)

            total_score += score

            for capture in regex_captures:
                if capture_convert:
                    capture = capture_convert(capture)

                capture_scores[capture] += score
                if self.DEBUG:
                    print("REGEX_SCORE: ", score)

        return matches, captures, total_score


class RegexHandler(object):
    """Used for matching and scoring sentences. Can be used by RegexClassifier
    """

    def __init__(self, return_ignores=False, preprocess_mode=PREPROCESS_PER_REGEX):
        self.DEBUG = False
        self.return_ignores = return_ignores
        self.preprocess_mode = preprocess_mode

    def score_data(self, text, regexes, pwds=None, preprocess_func=None, index_start=0):
        matches_score_dict, total_score = self.score_and_match_sentences(text, regexes, pwds=pwds, preprocess_func=preprocess_func,
                                                                         index_start=index_start)

        return matches_score_dict, total_score


    def score_and_match_sentences(self, text, regexes, pwds=None, preprocess_func=None,
                                  index_start=0):
        """Given regexes and text, determines a score for the sentence
        
        Arguments:
            text {String} -- Text to be split into sentences
            regexes {List} -- List of Regex Objects
        
        Returns:
            matches {dict} -- {sentence_i -> {"matches" -> list of modified match obj, "text_score": score (for sentence)}}
            total_score {int} -- Total score for the data
        """

        sentences = split_string_into_sentences(text)
        matches_score_dict = {}
        total_score = 0

        for i, sentence in enumerate(sentences):
            # Mimicing preprocessing from old tool

            if sentence == '':
                continue

            sentence = " {} ".format(sentence)

            preprocessed_data = {}

            if preprocess_func and self.preprocess_mode==PREPROCESS_BEFORE_REGEXES:
                preprocessed_data = preprocess_func(sentence)
            else:
                preprocessed_data["sentence"] = sentence
                preprocessed_data["dictionaries"] = pwds

            if preprocessed_data["sentence"] is None:
                continue

            matches, score = self.score_and_match_sentence(preprocessed_data["sentence"], regexes,
                                                           pwds=preprocessed_data["dictionaries"], preprocess_func=preprocess_func)

            # only adding sentences that matched
            if matches:
                if self.DEBUG:
                    print("Above results for sentence: ", i)
                matches_score_dict[i+index_start] = {"matches": matches, "text_score": score}

            total_score += score

        return matches_score_dict, total_score

    def score_and_match_sentence(self, text, regexes, pwds=None, preprocess_func=None):
        """Scores the text and returns matches based on the effects of the regexes
        
        Arguments:
            text {String} -- A string of text
            regexes {list} -- A list of Regex objects
        
        Returns:
            matches {list} -- List of match_objs Match_obj - {"name", "score", "effect", "matches": [MatchObj], "secondary_matches": [match_obj]} that matched with the text
            total_score {int} -- Score for the sentence

        """
        # Preprocessing sentence

        matches = []
        total_score = 0
        for regex in regexes:
            preprocessed_data = {}
            if preprocess_func and self.preprocess_mode == PREPROCESS_PER_REGEX:
                secondaries = regex.get_secondary_regexes()
                mentioned_pwds = set({secondary._required_pwds for secondary in secondaries})
                mentioned_pwds = list(set(regex._required_pwds) | mentioned_pwds)
                preprocessed_data = preprocess_func(text, *mentioned_pwds)
            else:
                preprocessed_data["sentence"] = text
                preprocessed_data["dictionaries"] = pwds

            if preprocessed_data["sentence"] is None:
                continue

            regex_matches = regex.determine_matches(preprocessed_data["sentence"], pwds=preprocessed_data["dictionaries"])
            score = regex.score*len(regex_matches)

            # Creating priority for regex effects. Ignores have highest precedence followed by replaces and lastly adds
            priority_queue = []
            secondary_matches = []
            primary_match = {"regex": regex, "name": regex.name, "score": regex.score, "effect": regex.effect, "matches": regex_matches, "pattern": regex.get_regex(), "secondary_matches": [], "aggregate_score": 0}

            add_primary_match = True

            # If the primary matches
            if len(regex_matches) > 0:

                # Getting all the secondary regexes grouped by effect
                ignore_regexes = regex.get_secondary_regexes(type_list=["i", "ib", "ia"])
                replace_regexes = regex.get_secondary_regexes(type_list=["r", "rb", "ra"])
                add_regexes = regex.get_secondary_regexes(type_list=["a", "ab", "aa"])

                # print(regex.get_secondary_regexes())

                # Pushing secondary regexes on to priority queue. Priority queue key is determined by order of appearance in secondary_regexes list and also their effect
                for i, secondary_regex in enumerate(ignore_regexes): heappush(priority_queue, (i, secondary_regex))
                for i, secondary_regex in enumerate(replace_regexes): heappush(priority_queue, (i+len(ignore_regexes), secondary_regex))
                for i, secondary_regex in enumerate(add_regexes): heappush(priority_queue, (i+len(ignore_regexes) + len(replace_regexes), secondary_regex))

                if self.DEBUG:
                    print("Regex: ", regex.get_regex())
                    print("TEXT: ", text)
                    print("Before filter:", regex_matches)
                    print("IGNORE REGEXES:", ignore_regexes)
                    print("REPLACE REGEXES:", replace_regexes)
                    print("ADD REGEXES:", add_regexes)
                    print("PRIORITY QUEUE:", priority_queue)

                for i in range(len(priority_queue)):
                    # Pop the secondary regex off the queue and compute the secondary matches
                    secondary_regex = heappop(priority_queue)[1]
                    secondary_regex_obj = {"name": secondary_regex.name, "effect": secondary_regex.effect, "pattern": secondary_regex.get_regex(), "score": secondary_regex.score, "matches": []}
                    secondary_match = match_secondary(secondary_regex, preprocessed_data["sentence"], regex_matches, pwds=preprocessed_data["dictionaries"])


                    # If there was a secondary match
                    if secondary_match:
                        if self.DEBUG:
                            print("After filter", regex_matches)
                            print("Secondary Match: ", secondary_match)
                        # Update secondary_regex_obj matches component
                        secondary_regex_obj["matches"] = secondary_match
                        # Add the secondary_regex_obj to the list of secondary_matches for the primary_regex_obj
                        secondary_matches.append(secondary_regex_obj)

                        # If ignore, stop eval of remaining secondary regexes
                        if secondary_regex.effect.startswith("i"):
                            score = 0
                            add_primary_match = self.return_ignores
                            break

                        # If replace, replace score and stop eval of remaining secondary regexes
                        elif secondary_regex.effect.startswith("r"):
                            score = secondary_regex.score

                        # If add, add to the score
                        elif secondary_regex.effect.startswith("a"):
                            score += secondary_regex.score

                    else:
                        if secondary_regex.effect.startswith("r"):
                            break

                # Setting primary regex's secondary matches param
                primary_match["secondary_matches"] = secondary_matches
                primary_match["aggregate_score"] = score

                # Add the primary regex to the list of matches for the sentence
                if add_primary_match:
                    matches.append(primary_match)

                if self.DEBUG:
                    print("REGEX_SCORE: ", score)


            total_score += score

        return matches, total_score
