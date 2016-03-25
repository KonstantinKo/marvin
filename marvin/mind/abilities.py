from marvin.support.log import Log
import marvin.support.regex_distance
import marvin.mind.ability
import marvin.mind.output_engine
import marvin.mind.speech_to_text

class Abilities(object):
    """
        Describes and works with a set of learned abilities, taught through
        instruction files by the community of developers.
    """

    def __init__(self, configs):
        self._stt = marvin.mind.speech_to_text.STT(configs)
        self._output_engine = marvin.mind.output_engine.OutputEngine()
        self.flags = []
        self._abilities = []
        for name, instructions in configs['abilities'].items():
            self._abilities.append(
                marvin.mind.ability.Ability(name, instructions))
        self._expect_immediate_answer = False

    def handle_app_start(self):
        """
            As a "special" static ability, notify the user via output engine
            that the app is ready to receive input
        """
        self._output_engine.say('Start')

    def handle_app_stop(self):
        """
            As a "special" static ability, notify the user via output engine
            that the app is closing down
        """
        self._output_engine.say('Goodbye')

    def handle_audio_input(self, audio):
        text = self._stt.transcribe(audio)
        if self._should_handle_audio(text):
            self.handle_text_input(text)
        else:
            Log.info('Heard "{}" - But answer requirements were not met', text)

    def handle_text_input(self, text):
        ability = self._find_ability_to_handle(text)
        if ability:
            self._respond_with_ability(ability, text)
        else:
            Log.info("No ability found for: {}", text)

    ### PRIVATE ###

    def _should_handle_audio(self, text):
        # return True # uncomment for debugging purposes
        return self._expect_immediate_answer or text.find('MARVIN') >= 0

    def _find_ability_to_handle(self, text):
        matching_abilities = []
        for ability in self._abilities:
            if ability.condition and ability.condition not in self.flags:
                continue

            score = ability.match(text)
            if score > -1:
                matching_abilities.append({'ability': ability, 'score': score})

        if len(matching_abilities) > 0:
            sorted_matches = sorted(
                matching_abilities, key=lambda k: k['score'])
            return sorted_matches[0]['ability']
        else:
            return None

    def _find_ability_by_name(self, ability_name):
        for ability in self._abilities:
            if ability.name == ability_name:
                return ability
        Log.err('Ability "{}" not found', ability_name)

    def _respond_with_ability(self, ability, text, forwarded = False):
        output_instructions = ability.response(forwarded)
        self._output_engine.say(output_instructions.get('say'))
        self.flags = [ability.name, output_instructions.get('set')]
        if 'act' in output_instructions: print(output_instructions.get('act'))
        self._expect_immediate_answer = ability.expect_immediate_answer

        if ability.forward:
            next_ability = self._find_ability_by_name(ability.forwarded_to())
            self._respond_with_ability(next_ability, text, True)

        if not forwarded:
            Log.info('Ability "{0}" successfully handled phrase "{1}"',
                     ability.name, text)
