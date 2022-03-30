from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import datetime
import pyttsx3
import speech_recognition as sr
import os.path
CREDENTIALS_FILE = r'C:\Users\shann\env\jarvis\credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'path_to_file/credentials.json'

def test(weekday):
    #is day passed yet
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_date(weekday):
    if 'monday' in weekday:
        return(test(0))
    elif 'tuseday' in weekday:
        return(test(1))
    elif 'wednesday' in weekday:
        return(test(2))
    elif 'thursday' in weekday:
        return(test(3))
    elif 'friday' in weekday:
        return(test(4))
    elif 'saturday' in weekday:
        return(test(5))
    elif 'sunday' in weekday:
        return(test(6))


def get_calendar_service():
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service

def get_calender():
   service = get_calendar_service()
   # Call the Calendar API
   calendars_result = service.calendarList().list().execute()

   calendars = calendars_result.get('items', [])

   if not calendars:
       return 'No calendars found.'
   for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       primary = "Primary" if calendar.get('primary') else ""
       return "%s\t%s\t%s" % (summary, id, primary)

def get_events(time):
    try:
        service = get_calendar_service()
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        if not 'bleh' in time:
            if 'tomorrow' in time:
                now = tomorrow

        print('Getting List o 10 events')
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    except Exception:
        return("There was an issue ")



def add_event():
    # creates one hour event tomorrow 10 AM IST
    service = get_calendar_service()

    d = datetime.now().date()
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": 'Automating calendar',
                                               "description": 'This is a tutorial example of automating google calendar with python',
                                               "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                                               "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                                           }
                                           ).execute()

    print("created event")
    return "id: ", event_result['id'], "summary: ", event_result['summary'], "starts at: ", event_result['start']['dateTime'],"ends at: ", event_result['end']['dateTime']

def delete_event():
       # Delete the event
       service = get_calendar_service()
       try:
           service.events().delete(
               calendarId='primary',
               eventId='<place your event ID here>',
           ).execute()
       except googleapiclient.errors.HttpError:
           print("Failed to delete event")

       print("Event deleted")

def update_event():
    # update the event to tomorrow 9 AM IST
    service = get_calendar_service()

    d = datetime.now().date()
    tomorrow = datetime(d.year, d.month, d.day, 9) + timedelta(days=1)
    start = tomorrow.isoformat()
    end = (tomorrow + timedelta(hours=2)).isoformat()

    event_result = service.events().update(
        calendarId='primary',
        eventId='<place your event ID here>',
        body={
            "summary": 'Updated Automating calendar',
            "description": 'This is a tutorial example of automating google calendar with python, updated time.',
            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
        },
    ).execute()

    return "id: ", event_result['id'], "summary: ", event_result['summary'], "starts at: ", event_result['start']['dateTime'],"ends at: ", event_result['end']['dateTime']




