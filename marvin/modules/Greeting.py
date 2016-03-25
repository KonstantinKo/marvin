# -*- coding: utf-8-*-
"""
    Basic module template.
"""


import re

SENTENCES = [
    "hello {P}", "hi {P}", "good morning {P}", "good afternoon {P}",
    "good evening {P}", "good day {P}"
]


def handle(text, output, profile):
    """
        Responds to user-input, typically speech text, by greeting the user.

        Arguments:
        text -- user-input, typically transcribed speech
        output -- engine used to converse with the user
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    output.say('Hello')

def isValid(text):
    """
        Returns True if the input is a greeting.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bhello\b', text, re.IGNORECASE))
