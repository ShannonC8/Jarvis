from __future__ import print_function
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import datetime
import os.path
import dateutil.parser
import utils
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
CREDENTIALS_FILE = r'C:\Users\shann\env\credentials.json'
from google.oauth2.credentials import Credentials
SCOPES = ['https://www.googleapis.com/auth/calendar']
month = [['j',0], ['january',1],['feburary',2],['march',3],['april',4],['may',5],
         ['june',6],['july',7], ['august',8], ['september',9], ['october',10],
         ['november',11], ['december',12]]

def test(weekday, time):
    #is day passed yet
    d = datetime.datetime.now().date()
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:  # Target day already happened this week
        days_ahead += 7

    day = d + datetime.timedelta(days_ahead)
    format = "%Y-%m-%d %H:%M:%S"
    dt_string = f"{day} {int(time)}:{int(00)}:{int(00)}"
    dt_object = datetime.datetime.strptime(dt_string, format)
    return dt_object

def get_date(weekday, time):
    d = datetime.datetime.now().date()
    if 'monday' in weekday:
        return((test(0, time)))
    elif 'tuseday' in weekday:
        return((test(1, time)))
    elif 'wednesday' in weekday:
        return((test(2, time)))
    elif 'thursday' in weekday:
        return((test(3, time)))
    elif 'friday' in weekday:
        return((test(4, time)))
    elif 'saturday' in weekday:
        return((test(5, time)))
    elif 'sunday' in weekday:
        return((test(6, time)))
    else:
        for day in month:
            if day[0] in weekday:
                format = "%Y-%m-%d %H:%M:%S"
                dt_string = f"{d.year}-{day[1]}-{(''.join(filter(str.isdigit, weekday.replace(day[0], ''))))} {int(time)}:{int(00)}:{int(00)}"
                dt_object = datetime.datetime.strptime(dt_string, format)
                return dt_object
               # return datetime(d.year, day[0], (''.join(filter(str.isdigit, weekday.replace(day[0], '')))), time)

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

def get_calendar():
    total = []
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting List of 3 events')
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=3, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date')) #time of event
        eventy = event['summary']#nme of event
        time = parsedDate = dateutil.parser.parse(start)
        eventys = f'you have{eventy} on {month[int(str(time)[5:7])][0]} {str(time)[8:10]}'
        print(time, event['summary'])
        total.append(eventys)
    return(total)

def add_event(event_name, event_date, event_time, event_length, event_description):
    try:
        service = get_calendar_service()
        # try:
        # d = datetime.now().date() datetime.datetime.now()
        start = get_date(event_date, event_time)
        end = get_date(event_date, int(event_time) + int(event_length))
        d = datetime.datetime.now().date()
        print(d.isoformat())
        print(start.isoformat())
        event_result = service.events().insert(calendarId='primary',
                                               body={
                                                   "summary": event_name,
                                                   "description": event_description,
                                                   "start": {"dateTime": start.isoformat(),
                                                             "timeZone": 'America/New_York'},
                                                   "end": {"dateTime": end.isoformat(), "timeZone": 'America/New_York'},
                                               }
                                               ).execute()
        print("id: ", event_result['id'], "summary: ", event_result['summary'], "starts at: ", event_result['start'][
            'dateTime'], "ends at: ", event_result['end']['dateTime'])
        return "created event"
    except Exception:
      return"something went wrong"


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




