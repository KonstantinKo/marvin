import random
import re

import marvin.support.lib
import marvin.support.regex_distance

class Ability(object):
    """
        A specific ability that enables Marvin to respond to input.
    """

    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions
        self.condition = self._get_optional_instruction('if')
        self.forward = self._get_optional_instruction('forward')
        self.regex = self._compile_regex()
        self.responses = self._prepare_responses()
        self.prefixes = self._prepare_prefixes()
        self.expect_immediate_answer = \
            self._get_optional_instruction('expect_immediate_answer')

    def match(self, text):
        return marvin.support.regex_distance.regex_score(self.regex, text)

    def response(self, forwarded):
        response = random.choice(self.responses).copy()

        if (not forwarded) and self.prefixes:
            response['say'] = "{0} - {1}".format(
                random.choice(self.prefixes), response['say'])

        return response

    def forwarded_to(self):
        return random.choice(self.forward)


    def _compile_regex(self):
        return re.compile(self.instructions['query']['regex'], re.IGNORECASE)

    def _prepare_responses(self):
        responses = self._normalize_list(self.instructions['response'])
        return list(map(self._normalize_response, responses))

    def _normalize_response(self, response):
        """
            Response can be given as string or set of output instructions.
            A string will be transformed to a single output instruction.
            Empty output instructions will be set to None.
        """
        if isinstance(response, str):
            return {'say': response, 'set': None, 'act': None}
        else:
            response.setdefault('say')
            response.setdefault('set')
            response.setdefault('act')
            return response

    def _prepare_prefixes(self):
        if 'prefix' in self.instructions:
            return self._normalize_list(self.instructions['prefix'])
        else:
            return None

    def _normalize_list(self, attribute):
        if isinstance(attribute, list):
            # flatten list in case aliases were used
            return marvin.support.lib.flatten(attribute)
        else:
            # make non-list into a list of one
            return [attribute]

    def _get_optional_instruction(self, key):
        return self.instructions[key] if (key in self.instructions) else None
