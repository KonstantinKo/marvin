import pyaudio
import subprocess
import tempfile
import wave

class Speaker(object):
    def output(self, text):
        wav_file = OSXTTS().convert(text)
        # self.play_wav(wav_file)

    def play_wav(self, wav_file):
        chunk = 1024
        opened_wav = wave.open(wav_file, 'rb')
        p = pyaudio.PyAudio()
        stream_format = p.get_format_from_width(opened_wav.getsampwidth())
        stream = p.open(format=stream_format,
                        channels=opened_wav.getnchannels(),
                        rate=opened_wav.getframerate(),
                        output=True)

        print('Start replaying audio\a')
        # read data
        data = opened_wav.readframes(chunk)

        # play stream
        while data != b'':
            stream.write(data)
            data = opened_wav.readframes(chunk)

        stream.close()
        p.terminate()
        print('Stop playing audio\a')
        subprocess.call(['rm', wav_file])

class AbstractTTS(object):
    def convert(self, text):
        raise "TTS ENgine needs to define the `convert` function"

class OSXTTS(AbstractTTS):
    def convert(self, text):
        subprocess.call(['say', text])

class FliteTTS(AbstractTTS):
    def convert(self, text):
        input_file = tempfile.NamedTemporaryFile('w+', suffix='.txt')
        input_file.write(text)
        input_file.seek(0)

        # output_file = tempfile.NamedTemporaryFile('w+b', suffix='.wav')
        filename = '/Data/Programmierung/Python/marvin/flitestuff.wav'
        subprocess.call(
            ['flite', input_file.name, filename])
        # output_file.seek(0)
        return filename

class MaryTTS(AbstractTTS):
    def convert(self, text):
        subprocess.call(['mary-client', text]) # vronk
