
import pyttsx3

class Speech:

    def __init__(self):
        self.engine = pyttsx3.init()


    def say(self, _text):
        self.engine = pyttsx3.init()
        self.engine.say(_text)
        self.engine.runAndWait()
