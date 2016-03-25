from marvin.support.log import Log
# import marvin.mind.sensory_input
import marvin.mind.abilities
import marvin.mind.output_engine
# import marvin.mind.processor
import marvin.body.input.stdin
import marvin.body.input.microphone

class Marvin(object):
    def __init__(self, configs):
        self.configs = configs
        # for key, config in configs.items():
        #     setattr(self, key, config)

        # self.sensory_input = marvin.mind.sensory_input.SensoryInput()
        self._input_modules = [
            marvin.body.input.stdin.Stdin(),
            marvin.body.input.microphone.Microphone()
        ]
        self.abilities = marvin.mind.abilities.Abilities(configs)
        # self.processor = marvin.mind.processor.Processor(
        #     self.output_engine, configs)

    def perform_startup_checks(self):
        Log.info('checking')

    def run(self):
        try:
            self.abilities.handle_app_start()

            for module in self._input_modules:
                module.start_evaluation(self.abilities)
            import time
            # Keep this process alive:
            while True: time.sleep(1)

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.abilities.handle_app_stop()

        for module in self._input_modules:
            module.shutdown()
