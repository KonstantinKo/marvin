# correct place?

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

from marvin.support.path import HMM_PATH

class STT(object):
    def __init__(self, app_configs):
        decoder_config = Decoder.default_config()
        decoder_config.set_string('-hmm', HMM_PATH + '/cmusphinx-en-us-5.2')
        decoder_config.set_string('-lm', app_configs['language_model'].name)
        decoder_config.set_string('-dict', HMM_PATH + '/cmudict.0.7a_SPHINX_40')
        decoder_config.set_string('-logfn', '/dev/null') # disable logging
        self._decoder = Decoder(decoder_config)

    def transcribe(self, data):
        self._decoder.start_utt()
        for chunk in data:
            self._decoder.process_raw(chunk, False, False)
        self._decoder.end_utt()

        hypothesis = self._decoder.hyp()
        segs = self._decoder.seg()
        if hypothesis:
            print("Recognized Segments:", [seg.word for seg in segs])
            print("Best Guess:", hypothesis.hypstr)
            return hypothesis.hypstr
        else:
            print("Nothing recognized.")
            return 'x'
