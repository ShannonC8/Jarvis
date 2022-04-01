import requests
from functions.online_ops import find_my_ip, get_latest_news, get_trending_movies, \
    get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, play_song, play_playlist, get_random_joke,\
    wolfram
from functions.calender import get_calendar_service, get_calendar, add_event, delete_event, update_event, get_date
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, close_camera, volume_change, pause, start_over
from random import choice
from utils import opening_text, response
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#TO DO:
# add to calender
# search and find amaon


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

last_query =""
last_answer=""

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
            if (not 'hey Jarvis'in query or 'listening' in query) and (runer == True) :
                print(query)
                speak(choice(opening_text))
                    #MIGHT BE ERROR
            else:
                if ('hey Jarvis' in query):
                    runer = True
                    speak(choice(response))
        else:
            hour = datetime.now().hour
            if hour >= 20 and hour < 6:
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
        last_query = query
        if 'repeat' in query and runer == True:
            speak(last_answer)

        if 'that' in query and runer == True:
            try:
                query = query.replace('that', last_answer)
            except Exception:
                query = query

        if 'open notepad' in query and runer == True:
            open_notepad()
            runer = False

        elif ('write' in query or 'take' in query)  and 'note' in query and runer == True:

            title = ask_question('What do you want to title it?')
            try:
                f = open(rf"C:\Users\shann\env\notes\{title}.txt", "x")
            except Exception:
                n = ask_question("that file already exists, would you like to overwrite it?")
                if 'yes' in n:
                    f = open(f"{title}.txt", "r+")
                elif 'add' in n:
                    f = open(f"{title}.txt", "a")
                else:
                    runer = False
                    break
            while True:
                content = ask_question('What do you want to write?')
                f.write(f'{content}\n')
                finish = ask_question('Do you want to continue?')
                if 'no' in finish:
                    f.close()
                    runer = False
                    break

        elif ('calendar' in query and 'add' in query) and runer == True:
            event_name = ask_question('What would you like to title the event?')
            event_date = ask_question('What date is the event?')
            event_time = ask_question('What time is the event? Please answer with a number in military time')
            event_length = ask_question('How many hours is the event?')
            event_description = ask_question('What is the description of the event?')
            speak(add_event(event_name,event_date,event_time,event_length,event_description))
            runer = False

        elif 'calendar' in query and runer == True:
            speak(get_calendar())
            last_answer = get_calendar()
            runer = False

        elif 'command' in query and 'open' in query and runer == True:
            open_cmd()
            runer = False

        elif 'open camera' in query and runer == True:
            open_camera()
            runer = False

        elif 'close camera' in query and runer == True:
            close_camera()
            runer = False

        elif 'open calculator' in query and runer == True:
            open_calculator()
            runer = False

        elif 'ip address' in query and runer == True:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen.')
            print(f'Your IP Address is {ip_address}')
            last_answer = ip_address
            runer = False

        elif 'wikipedia' in query and runer == True:
            search_query = ask_question('What do you want to search on Wikipedia?')
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen.")
            last_answer = results
            print(results)
            runer = False

        elif 'start over' in query:
            start_over()
            runer = False

        elif ('stop'in query or 'start' in query) and runer == True:
            pause()
            runer = False

        elif ('song' in query or 'music' in query) and runer == True:
            song = ask_question(f"what song would you like to play?")
            play_song(song)
            runer = False

        elif 'playlist' in query and runer == True:
            playlist = ask_question(f"what playlist would you like to play?")
            play_playlist(playlist)
            runer = False

        elif ('youtube' in query or 'video' in query or 'play' in query) and runer == True:
            #video = ask_question('What video do you want to play?')
            try:
                if 'play' in query:
                    query.rsplit('play')[1]
                query.replace('youtube','')
                play_on_youtube(query)
                runer = False
            except Exception:
                print(Exception)
                speak("not a valid search")
                runer = False

        elif ('google' in query or 'look up' in query) and runer == True:
            if "look up" in query:
                query = query.rsplit('look up')[1]
            elif 'google' in query:
                query = query.split('google', 1)[1]
            try:
                search_on_google(query)
                runer = False
            except Exception:
                print("not a valid question")
                runer = False

        elif 'how' in query and runer == True:
            search_on_google(query)
            runer = False

        elif 'joke' in query and runer == True:
            speak(f"Hope you like this one ")
            joke = get_random_joke()
            speak(joke)
            last_answer = joke
            runer = False

        elif ('Wikipedia' in query or 'who' in query) and runer == True:
            results = search_on_wikipedia(query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen.")
            print(results)
            last_answer = results
            runer = False

        elif "send an email" in query and runer == True:
            speak("On what email address do I send? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            subject = ask_question("What should be the subject?")
            message = ask_question("What is the message?")
            if send_email(receiver_address, subject, message):
                speak(f"the message is{message}")
                speak(f"the subject is{subject}")
                yn = ask_question("would you like to send it?")
                if 'yes' in yn:
                    speak("I've sent the email .")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs")
            runer = False

        elif "trending movies" in query and runer == True:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen.")
            print(*get_trending_movies(), sep='\n')
            last_answer = get_trending_movies()
            runer = False

        elif 'news' in query and runer == True:
            speak(f"I'm reading out the latest news headlines")
            news = get_latest_news()
            speak(news)
            speak("For your convenience, I am printing it on the screen")
            print(*get_latest_news(), sep='\n')
            last_answer = news
            runer = False

        elif 'weather' in query and runer == True:
            ip_address = find_my_ip()
            try:
                city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                speak(f"I'm getting weather report for your city {city}")
                weather, temperature, feels_like = get_weather_report(city)
                speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                speak("For your convenience, I am printing it on the screen.")
                print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
            except Exception:
                speak("something went wrong, try again later")
            runer = False

        elif 'date' in query and runer == True:
            speak(datetime.now())
            last_answer = datetime.now()
            speak("I am printing it on the screen as well.")
            print(datetime.now())
            runer = False

        elif ('lower' in query or 'softer' in query or 'quiter' in query or 'down' in query) and runer == True:
            if 'a lot' in query:
                n = volume_change(-12.0)
            else:
                n = volume_change(-6.0)
            if n == "not possible":
                speak("I cannot lower it anymore")
            else:
                speak("the volume has been raised")
            runer = False

        elif( 'raise' in query or 'louder' in query or 'up' in query) and runer == True:
            if 'a lot' in query:
                n = volume_change(12.0)
            else:
                n = volume_change(6.0)
            if n == "not possible":
                speak("I cannot raise it anymore")
            else:
                speak("the volume has been raised")
            runer = False

        elif 'what' in query and runer == True:
            speak(wolfram(query))
            last_answer = wolfram(query)
            runer = False

        elif runer == True and query != 'none' and (not 'hey jarvis' in query):
            speak(f"I do not understand what you mean by {query}, please restate your meaning")






