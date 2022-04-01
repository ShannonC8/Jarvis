import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
#from __future__ import print_function
import datetime
import os.path
import wolframalpha
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
NEWS_API_KEY = config("NEWS_API_KEY")
TMDB_API_KEY = config("TMDB_API_KEY")
API_KEY = config("WOLFRAM_ID")
SCOPES = ['https://www.googleapis.com/auth/calendar']

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def play_on_youtube(video):
    kit.playonyt(video)

def play_song(song):
    kit.playonyt(f"{song}song")

def play_playlist(playlist):
    kit.playonyt(f"{playlist}playlist")

def search_on_google(query):
    kit.search(query)

def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

#def create_event():
    #try:

#In the above method, we're first creating an empty list called news_headlines.
# We are then making a GET request on the API URL specified in the NewsAPI Documentation.

#Since the news is contained in a list called articles, we are creating a variable articles with the value res['articles'].
# Now we are iterating over this articles list and appending the article["title"]
# to the news_headlines list. We are then returning the first five news headlines from this list.
def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

def wolfram(uery):
    client = wolframalpha.Client(API_KEY)
    try:
        res = client.query(uery)
        result = next(res.results).text
        print(result)
        return(result)
    except Exception:
        return("No results")



