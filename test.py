import os.path
from datetime import datetime, timedelta
import pytz # To match timezones across all functions and files

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

event = {
    'summary': "testcase",
    'location': 'NTHU',
    'description': "test",
    'start': {
        'dateTime': "2026-04-07T13:00:00+08:00",
        'timeZone': 'Asia/Taipei',
    },
    'end': {
        'dateTime': "2026-04-07T15:00:00+08:00",
        'timeZone': 'Asia/Taipei',
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
}

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json")

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

try:
    service = build("calendar", "v3", credentials=creds) 

    event = service.events().insert(calendarId='4de43edb31f4137cd7f9bd5acabe09febac29f8d5c9ee9c7ff532e2fb8f47ca3@group.calendar.google.com', body=event).execute()

    print('Task/Event created succesfully')

except HttpError as error:
    print("An error occurred:", error)