import os.path
from datetime import datetime, timedelta
import pytz # To match timezones across all functions and files

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def checkCalendarList(service):
    calendars = service.calendarList().list().execute()

    for cal in calendars["items"]:
        print(cal["summary"], "→", cal["id"])

def extractPresent():
    taipei = pytz.timezone("Asia/Taipei")
    now = datetime.now(taipei)

    now = now.replace(microsecond=0)
    now = now.isoformat()

    return now

def extractDays(days):
    dayStr = ""
    for idx, day in enumerate(days):
        if idx == len(days)-1:
            dayStr += day
        else:
            dayStr = dayStr + day + ','

    return dayStr
        

def addOne(dt):
    start_date = datetime.strptime(dt, "%Y-%m-%d")

    # 2. add 1 day
    end_date = start_date + timedelta(days=1)

    # 3. datetime → string
    end_date_str = end_date.strftime("%Y-%m-%d")

    return end_date_str

def load_calendar_mapping(file_path):
    calendar_dict = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            # split only once (important)
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                name, cal_id = parts
                calendar_dict[name] = cal_id

    return calendar_dict

'''
def testCalendar():
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
        
        calendars = service.calendarList().list().execute()

        for cal in calendars["items"]:
            print(cal["summary"], "→", cal["id"])
        
        event = {
            'summary': 'event_testing',
            'location': 'NTHU',
            'description': 'Testing events using Google Calendar API',
            'start': {
                'dateTime': '2026-03-28T09:00:00+08:00',
                'timeZone': 'Asia/Taipei',
            },
            'end': {
                'dateTime': '2026-03-28T15:00:00+08:00',
                'timeZone': 'Asia/Taipei',
            },
            'attendees': [
                {'email': 'edbert.ls2004@gmail.com'},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        
        event = service.events().insert(calendarId='4de43edb31f4137cd7f9bd5acabe09febac29f8d5c9ee9c7ff532e2fb8f47ca3@group.calendar.google.com', body=event).execute()
        print('Event created: %s')

    except HttpError as error:
        print("An error occurred:", error)
'''

def task(rawJS):
    event = {
        'summary': rawJS['title'],
        'location': 'NTHU',
        'description': rawJS['notes'],
        'start': {'date': f'{rawJS['startDate']}'},
        'end': {'date': f'{addOne(rawJS['endDate'])}'},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    return event

def period(rawJS):

    if rawJS['recurring'] == True:
        event = {
            'summary': rawJS['title'],
            'location': 'NTHU',
            'description': rawJS['notes'],
            'start': {
                'dateTime': f"{rawJS['startDate']}T{rawJS['startTime']}:00+08:00",
                'timeZone': 'Asia/Taipei',
            },
            'end': {
                'dateTime': f"{rawJS['endDate']}T{rawJS['endTime']}:00+08:00",
                'timeZone': 'Asia/Taipei',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
            'recurrence': [
                f"RRULE:FREQ=WEEKLY;BYDAY={extractDays(rawJS['recurrence_days'])};UNTIL={rawJS['until']}T235959Z"
            ]
        }
    else:
        event = {
            'summary': rawJS['title'],
            'location': 'NTHU',
            'description': rawJS['notes'],
            'start': {
                'dateTime': f"{rawJS['startDate']}T{rawJS['startTime']}:00+08:00",
                'timeZone': 'Asia/Taipei',
            },
            'end': {
                'dateTime': f"{rawJS['endDate']}T{rawJS['endTime']}:00+08:00",
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

    #print("DEBUG: EVENT SENT\n", event, "\n\n")

    return event

def theCalendar(rawJS):
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

        checkCalendarList(service)

        if rawJS['endTime'] == None and rawJS['startTime'] == None:
            print("Task identified")
            event = task(rawJS)
        elif rawJS['endTime'] != None and rawJS['startTime'] != None:
            print("Period identified")
            event = period(rawJS)
        else:
            print("Wrong date format")
            return False
        
        calendars = load_calendar_mapping("calendars.txt")
    
        event = service.events().insert(calendarId=calendars[rawJS['category']], body=event).execute()

        print('Task/Event created succesfully')
        return True

    except HttpError as error:
        print("An error occurred:", error)
        return False

if __name__ == "__main__":
    theCalendar()