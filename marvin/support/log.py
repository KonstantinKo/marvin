class Log(object):
    """Logging helper, gives low character count aliases for the logging
    library and handles log routing in non-development environments
    """

    # colors
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @classmethod
    def info(self, *messages):
        print(Log.OKBLUE, "Info:", self._msg(messages), Log.ENDC)

    @classmethod
    def warn(self, *messages):
        print(Log.WARNING, "Warning:", self._msg(messages), Log.ENDC)

    @classmethod
    def err(self, *messages):
        print(Log.FAIL, "Error:", self._msg(messages), Log.ENDC)

    @classmethod
    def _msg(self, messages):
        if len(messages) > 1:
            return messages[0].format(*messages[1::])
        else:
            return messages[0]
