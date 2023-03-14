
import speech_recognition as sr

class Ear:

    def __init__(self):
        self.listener = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            self.listener.adjust_for_ambient_noise(source)
            audio_data = self.listener.listen(source)
            print("Recognizing...")
            text = self.listener.recognize_google(audio_data)
            return(text)