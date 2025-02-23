import pyttsx3
import speech_recognition as sr


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice' , voices[0].id)

def speak(audio):
               engine.say(audio)
               engine.runAndWait()

if __name__ == '__main__':
        speak("hello iam jarvis")

         