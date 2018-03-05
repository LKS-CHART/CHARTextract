from util.string_functions import split_string_into_sentences
from copy import copy

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

            total_score += score

            if len(regex_matches) > 0:
                #adding the new copied regex object to matches
                matches.append(regex_copy)



        return matches, total_score

