"""
Return the ordinal name of a number
Author: Winston Ewert
http://codereview.stackexchange.com/questions/41298/producing-ordinal-numbers
"""


def ordinal(num):
    SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

    # I'm checking for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix