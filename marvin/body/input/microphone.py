import marvin.body.input_module
import pyaudio
import collections
import math
import audioop

class Microphone(marvin.body.input_module.InputModule):
    SAMPLING_RATE = 16000
    CHUNK_SIZE = 1024
    SILENCE_WINDOW_LENGTH = 1 # Number of seconds, that if filled with no new
                              # input (silence) the current recording will be
                              # considered finished.

    PRERECORDING_LENGTH = .5  # Number of seconds to keep before a recording is
                              # started. These chunks will be prepended to the
                              # recording to prevent chopping the beginning of
                              # the phrase.

    CHUNKS_PER_SECOND = SAMPLING_RATE / CHUNK_SIZE

    def __init__(self):
        """Module startup: Setup and start audio stream from microphone"""
        self._audio = pyaudio.PyAudio()

        self._current_flag = pyaudio.paContinue

        self._reset_recording()

    def _reset_recording(self):
        self._current_recording = []
        self._is_currently_recording = False
        self._silence_window = collections.deque(
            maxlen=int(self.SILENCE_WINDOW_LENGTH * self.CHUNKS_PER_SECOND))
        self._prerecording = collections.deque(
            maxlen=int(self.PRERECORDING_LENGTH * self.CHUNKS_PER_SECOND))

    def start_evaluation(self, abilities):
        self._abilities = abilities
        self._stream = self._audio.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=self.SAMPLING_RATE,
                                        input=True,
                                        frames_per_buffer=self.CHUNK_SIZE,
                                        stream_callback=self.stream_callback)

    def shutdown(self):
        """Close and stop all module activity"""
        self._current_flag = pyaudio.paComplete
        self._stream.stop_stream()
        self._stream.close()
        self._audio.terminate()

    def stream_callback(self, current_chunk, frame_count, time_info, status):
        """ A tick in the process of listening for / recording user voice
            commands
        """
        # print('tick', frame_count, time_info, status_flags)
        # return (None, self._current_flag)

        current_intensity = self._get_sample_intensity(current_chunk)

        self._silence_window.append(current_intensity)
        # print('intensity:', current_intensity) #!

        if self._should_be_recording():
            if (not self._is_currently_recording):
                print("Start recording")
                self._is_currently_recording = True

            self._current_recording.append(current_chunk)

        elif self._is_currently_recording:
            print("Finished. Stop recording")
            self._finalize_and_analyse_recording()
            self._reset_recording()

        else: # neither already recording nor should be recording
            self._prerecording.append(current_chunk)

        return (None, self._current_flag)


    def _get_sample_intensity(self, chunk):
        """Get the sound intensity from a chunk of sample data"""
        return math.sqrt(abs(audioop.avg(chunk, 4)))

    # TODO: use dynamic threshold, voice frequencies, spectral flatness analysis
    def _should_be_recording(self):
        return sum([x > 1000 for x in self._silence_window]) > 0

    def _finalize_and_analyse_recording(self):
        # The limit was reached, finish capture and deliver.
        recording = list(self._prerecording) + self._current_recording
        # self.playThatData(recording) # TODO: only for debugging
        self._abilities.handle_audio_input(recording)





    # ---- cut ----


    # def listen(self):
    #     if False:
    #         return "Bla"
    #     else:
    #         return None
    #
    # def _listen(self):

    # In loop:
    # - get data chunk
    # - assume silence at the start of the loop
    # - calculate threshold from existing data
    # - below threshold: add to previous data collection
    # - above threshold: check if voice probable ? record : previous data
    # - no voice for X time? stop recording

    def listenTwo(self):
        self.audio_int()
        import collections
        import math
        import os
        num_phrases = 1


        THRESHOLD = 1500  # The threshold intensity that defines silence
                          # and noise signal (an int. lower than THRESHOLD is silence).

        SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                           # only silence is recorded. When this time passes the
                           # recording finishes and the file is delivered.

        PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                          # is detected, how much of previously recorded audio is
                          # prepended. This helps to prevent chopping the beginning
                          # of the phrase.

        #Open stream
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* Listening mic. ")
        audio2send = []
        current_data = ''  # current chunk of audio data
        rel = RATE/CHUNK # ?
        slid_win = collections.deque(maxlen=int(SILENCE_LIMIT * rel)) #?
        #Prepend audio from 0.5 seconds before noise was detected
        prev_audio = collections.deque(maxlen=int(PREV_AUDIO * rel))
        started = False
        n = num_phrases
        response = []

        while (num_phrases == -1 or n > 0):
            current_data = stream.read(CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(current_data, 4))))
            print('last in slid_win:', slid_win[-1])
            if(sum([x > THRESHOLD for x in slid_win]) > 0):
                if(not started):
                    print("Starting record of phrase")
                    started = True
                audio2send.append(current_data)
            elif (started is True):
                print("Finished / Stop recording")
                # The limit was reached, finish capture and deliver.
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                # Send file to Google and get response
                self.playThatShit(filename) #!
                r = 'Bla'
                if num_phrases == -1:
                    print("Response", r)
                else:
                    response.append(r)
                # Remove temp file. Comment line to review.
                os.remove(filename)
                # Reset all
                started = False
                slid_win = collections.deque(maxlen=int(SILENCE_LIMIT * rel))
                prev_audio = collections.deque(maxlen=int(0.5 * rel))
                audio2send = []
                n -= 1
                print("Listening ...")
            else:
                prev_audio.append(current_data)

        print("* Done recording")
        stream.close()
        p.terminate()

        return None #!
        return response


    def save_speech(self, data, p):
        """ Saves mic data to temporary WAV file. Returns filename of saved
            file """


        import time
        import wave


        filename = 'output_'+str(int(time.time()))
        # writes data to WAV file
        data = b''.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)  # TODO make this value a function parameter?
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'


    def audio_int(self, num_samples=50):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the 20% largest intensities recorded.
        """
        import math
        import audioop

        print("Getting intensity values from mic.")
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)

        values = [math.sqrt(abs(audioop.avg(stream.read(1024), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print(" Finished ")
        print(" Average audio intensity is ", r)
        stream.close()
        p.terminate()
        return r

    def listenOne(self, PERSONA = 'Marvin'):
        """
        Listens for PERSONA in everyday sound. Times out after LISTEN_TIME, so
        needs to be restarted.
        """

        THRESHOLD_MULTIPLIER = 1.8
        RATE = 16000
        CHUNK = 1024

        # number of seconds to allow to establish threshold
        THRESHOLD_TIME = 1

        # number of seconds to listen before forcing restart
        LISTEN_TIME = 10

        # prepare recording stream
        stream = self._audio.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        # stores the audio data
        frames = []

        # stores the lastN score values
        lastN = [i for i in range(30)]

        # calculate the long run average, and thereby the proper threshold
        print('Start recording for threshold')
        for i in range(0, int(RATE / CHUNK * THRESHOLD_TIME)):

            data = stream.read(CHUNK)
            frames.append(data)

            # save this data point as a score
            lastN.pop(0)


            # ! getScore
            rms = audioop.rms(data, 2)
            score = rms / 3


            lastN.append(score)
            average = sum(lastN) / len(lastN)

        # this will be the benchmark to cause a disturbance over!
        THRESHOLD = average * THRESHOLD_MULTIPLIER
        print('Stop recording for threshold')

        # save some memory for sound data
        frames = []

        # flag raised when sound disturbance detected
        didDetect = False

        # start passively listening for disturbance above threshold
        print('Start recording for input')
        for i in range(0, int(RATE / CHUNK * LISTEN_TIME)):

            data = stream.read(CHUNK)
            frames.append(data)


            # ! getScore
            rms = audioop.rms(data, 2)
            score = rms / 3



            if score > THRESHOLD:
                print('Bingo!')
                didDetect = True
                break

        # no use continuing if no flag raised
        if not didDetect:
            print("No disturbance detected")
            stream.stop_stream()
            stream.close()
            return None

        # cutoff any recording before this disturbance was detected
        frames = frames[-20:]

        # otherwise, let's keep recording for few seconds and save the file
        DELAY_MULTIPLIER = 1
        for i in range(0, int(RATE / CHUNK * DELAY_MULTIPLIER)):

            data = stream.read(CHUNK)
            frames.append(data)

        # save the audio data
        stream.stop_stream()
        stream.close()

        import tempfile # !!!
        import wave # !!!
        with tempfile.NamedTemporaryFile(mode='w+b') as f:
            wav_fp = wave.open(f, 'wb')
            wav_fp.setnchannels(1)
            wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
            wav_fp.setframerate(RATE)
            wav_fp.writeframes(b''.join(frames))
            wav_fp.close()
            f.seek(0)

            self.playThatShit(f)

            # check if PERSONA was said
        #     transcribed = self.passive_stt_engine.transcribe(f)
        #
        # if any(PERSONA in phrase for phrase in transcribed):
        #     return (THRESHOLD, PERSONA)

        # return (False, transcribed)
        return None

    def playThatShit(self, f):
        import wave # !!!
        chunk = 1024
        wf = wave.open(f, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        print('Start replaying audio\a')
        # read data
        data = wf.readframes(chunk)

        # play stream
        while data != b'':
            stream.write(data)
            data = wf.readframes(chunk)

        stream.close()
        p.terminate()
        print('Stop playing audio\a')

    def playThatData(self, data):
        import wave # !!!
        # chunk = 1024
        # wf = wave.open(f, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.SAMPLING_RATE,
                        output=True,
                        frames_per_buffer=self.CHUNK_SIZE)


        print('Start replaying data\a')
        # read data
        # data = wf.readframes(chunk)

        # play stream
        for chunk in data:
            stream.write(chunk)
            # data = wf.readframes(chunk)

        stream.close()
        p.terminate()
        print('Stop playing data\a')
