import re

def split_string_into_sentences(text):
    '''
    Given a string of text, splits it into sentences

    TODO: Add lookbehind for Mr. Ms. etc..
    :param text: A string
    :return: A string split into sentences
    '''

    return text.split(".")

def split_string_into_words(text):
    '''
    Given a string of text, splits it into individual words

    TODO: See if there is anyway to make it better

    :param text: A string
    :return: A string split into words
    '''

    return re.split(r"[?!\.\s/)(:#]+", text)
