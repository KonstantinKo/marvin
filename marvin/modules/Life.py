# -*- coding: utf-8-*-
import random
import re

SENTENCES = [
    "{P} What is the meaning of life {P}",
    "{P} Can you tell me what the meaning of life is {P}",
    "{P} Do you know what the meaning of life is {P}",
    "{P} I wonder the meaning of life is {P}"
]


def handle(text, output, profile):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        output -- engine used to converse with the user
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    messages = ["It's 42.",
                "It's 42. How many times do I have to tell you?"]

    message = random.choice(messages)

    output.say(message)


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bmeaning of life\b', text, re.IGNORECASE))
