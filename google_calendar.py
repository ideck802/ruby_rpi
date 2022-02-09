from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
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
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)


def search_for_event(search_term):
    today = str(datetime.datetime.now()).replace(" ","T") + "-06:00"
    print(today)
    return service.events().list(calendarId='primary', q=search_term, timeMin=today).execute().get('items', [])

def add_event(name, startDate, startTime, endDate, endTime): # dates use dashes (2020-01-30), time use military (16:10:00)
    event = {
      'summary': name,
      'start': {
        'dateTime': startDate + 'T' + startTime,
        'timeZone': 'America/Chicago',
      },
      'end': {
        'dateTime': endDate + 'T' + endTime,
        'timeZone': 'America/Chicago',
      }}
    event = service.events().insert(calendarId='primary', body=event).execute()