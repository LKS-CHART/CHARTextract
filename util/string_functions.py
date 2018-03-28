import re

def as_text(value):
    """Returns the string representation of given value
    
    Arguments:
        value {any} -- Value to get the string representation for
    
    Returns:
        stringified text {String} -- String representation of given value
    """

    return "" if value is None else str(value)

def split_string_into_sentences(text):
    """Given a string of text, splits it into sentences
    
    Arguments:
        text {string} -- A string
    
    Returns:
        sentence {list} -- A list of sentences
    """

    #TODO: Add lookbehind for Mr. Ms. etc..
    return text.split(".")

def split_string_into_words(text):
    """Given a string of text, splits it into words
    
    Arguments:
        text {string} -- A string
    
    Returns:
        sentence {list} -- A list of words
    """

    #TODO: Look at ways to make this better
    return re.split(r"[?!\.\s/)(:#]+", text)
