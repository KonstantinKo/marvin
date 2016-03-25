"""
    Module to calculate Levenshtein distances, and the distance between a set
    of regexes to a matching string.
"""

import re
import sre_parse

def levenshtein_distance(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n

    current = range(n+1)
    for i in range(1, m+1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n+1):
            add, delete = previous[j] + 1, current[j-1] + 1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]

def regex_score(regex, search_string):
    """
        Returns a closeness score of how well the regex matches the string.
        Will return -1 if it doesn't match.
    """

    match = re.search(regex, search_string)

    if match:
        # Base score is the longest distance between regex, match,
        # and search_string
        regex_match_dist = levenshtein_distance(
            regex.pattern.lower(), match.group(0).lower())
        match_string_dist = levenshtein_distance(
            match.group(0).lower(), search_string.lower())

        score = max(regex_match_dist, match_string_dist)

        # Adjust score: Special anchors slightly reduce distance
        for opcode, argument in sre_parse.parse(regex.pattern):
            if str(opcode) == 'AT':
                if str(argument) == 'AT_BEGINNING' or 'AT_END':
                    # ^ or $, adjust 1 edit
                    score -= 1

                if str(argument) == 'AT_BOUNDARY':
                    # all other anchors reduce 2 edits
                    score -= 2

        return score if score >= 0 else 0
    else:
        return -1
