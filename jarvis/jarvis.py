import sys
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow
from jarvisgui import Ui_MainWindow  # Ensure jarvisgui.py exists with Ui_MainWindow

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak('Good morning')
    elif 12 <= hour < 18:
        speak('Good afternoon')
    else:
        speak('Good night')
    speak("I am Jarvis, please tell me how I can help you")

def exit_program():
    speak("Goodbye! Have a great day.")
    exit()

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.taskexecution()

    def takecommand(self):
        """ Take voice command from user """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=8, phrase_time_limit=40)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
        except Exception as e:
            speak("Say that again, please...")
            return "none"

        return query

    def taskexecution(self):
        wish()
        while True:
            self.query = self.takecommand().lower()

            if 'open notepad' in self.query:
                os.startfile("C:\\Windows\\system32\\notepad.exe")

            elif 'open camera' in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('Webcam', img)
                    if cv2.waitKey(50) == 27:  # Press 'Esc' to exit
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif 'ip address' in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP address is {ip}")
                print(ip)

            elif 'wikipedia' in self.query:
                speak("Searching on Wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia...")
                print(results)
                speak(results)

            elif 'open youtube' in self.query:
                webbrowser.open('https://www.youtube.com/')

            elif 'open google' in self.query:
                speak("What should I search on Google?")
                cm = self.takecommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={cm}")

            elif 'play song on youtube' in self.query:
                   speak("What song do you want to play?")
                   gh = self.takecommand().lower()
    
                   if gh == "none":  # If no input is received
                      speak("I didn't hear the song name. Please try again.")
                   else:
                      speak(f"Playing {gh} on YouTube")
                      kit.playonyt(gh)  # Pass only the user-input song name
     

            elif 'exit' in self.query or 'stop' in self.query:
                exit_program()

startexecution = MainThread() 

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        """ Start Jarvis AI and update GUI animations """
        self.ui.movie = QMovie("../../Downloads/2141507-3840x1080-desktop-dual-monitors-jarvis-iron-man-wallpaper-image.jpg")  # Ensure this is a valid GIF
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        '''
       # Timer to update time & date
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
          '''

        # Start Jarvis thread
        startexecution.start()

'''

   def showTime(self):
        """ Update Time and Date on GUI """
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        self.ui.text_time.setText(current_time.toString("hh:mm:ss AP"))
        self.ui.text_date.setText(current_date.toString(Qt.ISODate))
          '''

# Run the application
app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())