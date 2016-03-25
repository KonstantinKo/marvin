import marvin.body.output.stdout
import marvin.body.output.speaker

class OutputEngine:
    def say(self, text):
        console = marvin.body.output.stdout.Stdout()
        console.output(text)
        speaker = marvin.body.output.speaker.Speaker()
        speaker.output(text)
