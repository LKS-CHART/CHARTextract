import functools
import operator

def combine_flags(flag_list):
    """Combines regex flags using bitwise or
    
    Arguments:
        flag_list {list} -- List of flags e.g [re.IGNORECASE, re.DEBUG]
    
    Returns:
        int -- Bitwise or of flags
    """

    #Or operator applied to flag_list
    return functools.reduce(operator.or_, flag_list)

