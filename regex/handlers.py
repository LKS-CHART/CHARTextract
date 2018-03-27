from util.string_functions import split_string_into_sentences
from itertools import product
from heapq import *
from collections import defaultdict

class CaptureHandler(object):
    #TODO: Only works with primary regexes not secondary. Add this functionality later... Should pretty much be identical
    #TODO: Add generic score_and_capture_text and have score_and_capture_sentence call that

    """Used for capturing and scoring sentences. Can be used by CaptureClassifier
    """

    def __init__(self):
        pass

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
        captures = {}
        capture_scores = defaultdict(int)

        #Scoring and capturing each sentence
        for i, sentence in enumerate(sentences):
            matches, captures, score = self.score_and_capture_sentence(sentence, regexes, capture_scores, pwds=pwds, preprocess_func=preprocess_func, capture_convert=capture_convert)

            if matches:
                matches_scores_dict[i] = {"matches": matches, "text_score": score}

        return matches_scores_dict, captures, capture_scores

    def score_and_capture_sentence(self, text, regexes, capture_scores, pwds=None, preprocess_func=None, capture_convert=None):
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

        #Preprocessing sentence
        if preprocess_func:
            text, preprocessed_pwds = preprocess_func(text, pwds)

        #For every regex we want to get the captures, matches and compute a score using the primary regex score
        for regex in regexes:

            #Getting matches and captures
            regex_matches, regex_captures = regex.determine_captures_w_matches(text, pwds=pwds)

            #If regex returns all the matches want to multiply score by length
            score = regex.score*len(regex_matches)

            #match_obj
            primary_matches = {"name": regex.name, "score": regex.score, "effect": regex.effect, "matches": regex_matches, "secondary_matches": []}

            #Converting the capture using the capture_convert function
            #E.g Canadian -> Canada, Trinidadian -> Trinidad
            for capture in regex_captures:
                if capture_convert:
                    capture = capture_convert(capture)

                capture_scores[capture] += regex.score

            #If matches we want to add the matches to the list of matches
            #Extending the list of all captured text
            if len(regex_matches) > 0:
                matches.append(primary_matches)
                captures.extend(regex_captures)

            #Adding the computed regex score to the running total for the sentence
            total_score += score

        return matches, captures, total_score


class RegexHandler(object):
    """Used for matching and scoring sentences. Can be used by RegexClassifier
    """

    def __init__(self):
        pass

    #TODO: Maybe create an effect handler
    def _match_secondary(self, secondary_regex, text, primary_regex_matches):
        """Computes matches for the secondary regex
        
        Arguments:
            secondary_regex {Regex} -- Secondary Regex object to compute the matches for
            text {String} -- Text to match
            primary_regex_matches {list} -- List of MatchObjs for primary regex
        
        Returns:
            secondary_matches {list} -- List of MatchObjs for secondary regex
        """

        #Getting secondary matches
        secondary_matches = secondary_regex.determine_matches(text)

        if secondary_matches:
            #If regex has a before or after effect e.g rb, ia etc.. do some extra checks based on effect
            #Otherwise, just return secondary_matches
            if len(secondary_regex.effect) == 2:
                effect_modifier = secondary_regex.effect[1]
                #If secondary match appears before any of the primary matches
                if effect_modifier == "b" and any(map(lambda tup: tup[0].start() < tup[1].start(), product(secondary_matches, primary_regex_matches))):
                    secondary_matches = secondary_matches
                #If it appears after any of the primary matches
                elif effect_modifier == "a" and any(map(lambda tup: tup[0].start() > tup[1].end(), product(secondary_matches, primary_regex_matches))):
                    secondary_matches = secondary_matches
                #If the above two were not satisfied, the secondary regex failed to satisfy its after effect
                else:
                    secondary_matches = []

        return secondary_matches

    def score_and_match_sentences(self, text, regexes):
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
            matches, score = self.score_and_match_sentence(sentence, regexes)

            #only adding sentences that matched
            if matches:
                matches_score_dict[i] = {"matches": matches, "text_score": score}

            total_score += score

        return matches_score_dict, total_score

    def score_and_match_sentence(self, text, regexes):
        """Scores the text and returns matches based on the effects of the regexes
        
        Arguments:
            text {String} -- A string of text
            regexes {list} -- A list of Regex objects
        
        Returns:
            matches {list} -- List of match_objs Match_obj - {"name", "score", "effect", "matches": [MatchObj], "secondary_matches": [match_obj]} that matched with the text
            total_score {int} -- Score for the sentence

        """
        matches = []
        total_score = 0
        for regex in regexes:
            regex_matches = regex.determine_matches(text)
            score = regex.score*len(regex_matches)

            #Creating priority for regex effects. Ignores have highest precedence followed by replaces and lastly adds
            priority_queue = []
            secondary_matches = []
            primary_match = {"name": regex.name, "score": regex.score, "effect": regex.effect, "matches": regex_matches, "pattern": regex.get_regex(), "secondary_matches": []}

            #If the primary matches
            if len(regex_matches) > 0:

                #Getting all the secondary regexes grouped by effect
                ignore_regexes = regex.get_secondary_regexes(type_list=["i", "ib", "ia"])
                replace_regexes = regex.get_secondary_regexes(type_list=["r", "rb", "ra"])
                add_regexes = regex.get_secondary_regexes(type_list=["a", "ab", "aa"])

                #Pushing secondary regexes on to priority queue. Priority queue key is determined by order of appearance in secondary_regexes list and also their effect
                for i, secondary_regex in enumerate(ignore_regexes): heappush(priority_queue, (i, secondary_regex))
                for i, secondary_regex in enumerate(replace_regexes): heappush(priority_queue, (i+len(ignore_regexes), secondary_regex))
                for i, secondary_regex in enumerate(add_regexes): heappush(priority_queue, (i+len(ignore_regexes) + len(replace_regexes), secondary_regex))

                for i in range(len(priority_queue)):
                    #Pop the secondary regex off the queue and compute the secondary matches
                    secondary_regex = heappop(priority_queue)[1]
                    secondary_regex_obj = {"name": secondary_regex.name, "effect": secondary_regex.effect, "pattern": regex.get_regex(), "score": secondary_regex.score, "matches": []}
                    secondary_match = self._match_secondary(secondary_regex, text, regex_matches)

                    #If there was a secondary match
                    if secondary_match:
                        #Update secondary_regex_obj matches component
                        secondary_regex_obj["matches"] = secondary_match
                        #Add the secondary_regex_obj to the list of secondary_matches for the primary_regex_obj
                        secondary_matches.append(secondary_regex_obj)

                        #If ignore, stop eval of remaining secondary regexes
                        if secondary_regex.effect.startswith("i"):
                            score = 0
                            break

                        #If replace, replace score and stop eval of remaining secondary regexes
                        elif secondary_regex.effect.startswith("r"):
                            score = secondary_regex.score
                            break

                        #If add, add to the score
                        elif secondary_regex.effect.startswith("a"):
                            score += secondary_regex.score

                #Setting primary regex's secondary matches param
                primary_match["secondary_matches"] = secondary_matches

                #Add the primary regex to the list of matches for the sentence
                matches.append(primary_match)

            total_score += score

        return matches, total_score
