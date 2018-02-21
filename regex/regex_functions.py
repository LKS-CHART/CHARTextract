import functools
import operator

def combine_flags(flag_list):
    '''
    Combines regex flags using bitwise or

    :param flag_list: list of flags e.g [re.IGNORECASE, re.DEBUG]

    :return: int

    '''

    return functools.reduce(operator.or_, flag_list)

