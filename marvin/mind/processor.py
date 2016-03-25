# import pkgutil
#
# from marvin.support.log import Log
# import marvin.support.path
#
# import marvin.mind.speech_to_text
#
# class Processor(object):
#     def __init__(self, output_engine, configs):
#         """
#         Instantiates a new Brain object, which cross-references user
#         input with a list of modules. Note that the order of brain.modules
#         matters, as the Brain will cease execution on the first module
#         that accepts a given input.
#
#         Arguments:
#         mic -- used to interact with the user (for both input and output)
#         configs -- contains information related to the user (e.g., phone
#                    number)
#         """
#
#         self.configs = configs
#         self.output_engine = output_engine
#         self.modules = configs['modules']
#         self._stt = marvin.mind.speech_to_text.STT(configs)
#         # self._logger = logging.getLogger(__name__)
#
#     def process_audio_input(self, audio):
#         result = self._stt.transcribe(audio)
#         self.query(result)
#
#     def query(self, text):
#         """
#         Passes user input to the appropriate module, testing it against
#         each candidate module's isValid function.
#
#         Arguments:
#         text -- user input, typically speech, to be parsed by a module
#         """
#         for module in self.modules:
#             if module.isValid(text):
#                 try:
#                     module.handle(text, self.output_engine, self.configs)
#                 except:
#                     Log.err('Failed to execute module {0}', module.__name__)
#                     # self.mic.say("I'm sorry. I had some trouble with " +
#                     #              "that operation. Please try again later.")
#                 else:
#                     Log.info("Module '{0}' successfully handled phrase '{1}'",
#                              module.__name__, text)
#                 finally:
#                     return
#         Log.info("No module was able to handle the phrase: {0}", text)
