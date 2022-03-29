import requests
from flask import Flask
from functions.online_ops import find_my_ip, get_latest_news, get_trending_movies, \
    get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, play_song, play_playlist, get_random_joke
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, close_camera, volume_change
from random import choice
from utils import opening_text
from pprint import pprint
import os
import json
import time
from pathlib import Path
from datetime import date, timedelta


USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 200)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()

def ask_question(question):
    while True:
        runer = True
        speak(question)
        answer, runer = take_user_input(runer)
        if (answer != 'None') == True:
            break
    answer = answer.lower()
    return answer

# Greet the user
def greet_user():
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    else:
        speak(f"Hello {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")


# Takes Input from User
def take_user_input(runer):
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        if runer == True:
            print('Listening....')
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        if runer == True:
            print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')#r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            if not 'for now' in query:
                if (not 'hey Jarvis'in query) and (runer == True) :
                    print(query)
                    speak(choice(opening_text))
                    #MIGHT BE ERROR
                else:
                    if('hey Jarvis' in query):
                        print("yes")
                        runer = True
                        speak("what's up?")
            else:
                runer = False
                speak("got it, let me know if you need Anything")
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night, take care!")
            else:
                speak('Have a good day bestie!')
            exit()
    except Exception:
        if runer == True:
          speak('Sorry, I could not understand. Could you please say that again?')
          query = 'None'
        else:
            speak("")
            query = 'None'
    return query, runer


if __name__ == '__main__':
    greet_user()
    runer = True
    while True:
        query, runer = take_user_input(runer)
        query = query.lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'close camera' in query:
            close_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            search_query = ask_question('What do you want to search on Wikipedia?')
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen.")
            print(results)

        elif 'youtube' in query or 'video' in query:
            video = ask_question('What video do you want to play?')
            play_on_youtube(video)

        elif 'google' in query :
            #quer =ask_question('What do you want to search on Google?')
            search_on_google(query.replace('google',''))

        elif 'how' in query :
            search_on_google(query)

        elif 'joke' in query:
            speak(f"Hope you like this one ")
            joke = get_random_joke()
            speak(joke)

        elif 'who' in query:
            results = search_on_wikipedia(query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen.")
            print(results)

        elif "send an email" in query:
            speak("On what email address do I send? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            subject = ask_question("What should be the subject?")
            message = ask_question("What is the message?")
            if send_email(receiver_address, subject, message):
                speak(f"the message is{message}")
                speak(f"the subject is{subject}")
                yn = ask_question("would you like to send it?")
                if yes in yn:
                    speak("I've sent the email .")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs")

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"I'm getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

        elif 'song' in query or 'music' in query:
            song = ask_question(f"what song would you like to play?")
            play_song(song)

        elif 'date' in query:
            speak(datetime.now())
            speak("I am printing it on the screen as well.")
            print(datetime.now())

        elif 'playlist' in query:
            playlist = ask_question(f"what playlist would you like to play?")
            play_playlist(playlist)

        elif 'thanks' in query or 'thank you' in query:
            speak(f"no problem")

##MKE ONE FUCNTION
        elif 'lower' in query or 'softer' in query or 'quiter' in query or 'down' in query:
            volume_chage(-6.0)

        elif 'raise' in query or 'louder' in query or 'up' in query:
            volume_change(6.0)

        elif 'set' in query and 'volume' in query:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            vol = ask_question("What volume would you like me to set it to?")
            if vol.is_integer():
                volume.SetMasterVolumeLevel(vol, None)
            else:
                speak("not a number")


