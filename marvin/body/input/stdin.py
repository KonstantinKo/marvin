import multiprocessing
import sys
import select

import marvin.body.input_module
from marvin.support.log import Log

class Stdin(marvin.body.input_module.InputModule):
    """stdin input module - The most basic input module

    This module should always be running, contains the only blocking loop that
    keeps the process alive, and is the only input module that should not be
    running as a separate child process.
    """

    def start_evaluation(self, abilities):
        self._abilities = abilities
        self._should_be_listening = True
        self._process = multiprocessing.Process(target=self.listen)
        self._process.start()

    def listen(self):
        try:
            sys.stdin = open(0)
            while self._should_be_listening:
                while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = sys.stdin.readline()
                    if line:
                        self._abilities.handle_text_input(line.strip())
        except KeyboardInterrupt:
            pass

    def shutdown(self):
        self._should_be_listening = False
        if self._process.is_alive():
            Log.warn('Process didnt shut down')
            self._process.terminate()
