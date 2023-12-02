from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from datetime import datetime

import os 

class google:
    def __init__(self, CALENDAR_ID) -> None:
        self.SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar.events.readonly", "https://www.googleapis.com/auth/calendar.events"]
        self.CALENDAR_ID = CALENDAR_ID

    def authenticate(self):
        creds = None
        if os.path.exists('token.json'): 
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token: 
                creds.refresh(Request())
            else: 
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json()) 
        return creds

    def service(self):
        creds = self.authenticate()
        return build('calendar', 'v3', credentials=creds)

    def create_event(self, summary, description, startDate, endDate):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': startDate, #2023-12-01T10:00:00
                'timeZone': 'Europe/Paris',
            },
            'end': {
                'dateTime': endDate,
                'timeZone': 'Europe/Paris',
            }
        }
        return self.service().events().insert(calendarId=self.CALENDAR_ID, body=event).execute()

    def get_events_from_today(self):
        today_date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S+01:00")
        events = self.service().events().list(calendarId=self.CALENDAR_ID, timeMin=today_date).execute()
        return events['items']

    def update_event(self, eventId, summary, description, startDate, endDate):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': startDate, #'2023-12-01T10:00:00
                'timeZone': 'Europe/Paris',
            },
            'end': {
                'dateTime': endDate,
                'timeZone': 'Europe/Paris',
            }
        }
        
        return self.service().events().update(calendarId=self.CALENDAR_ID, eventId=eventId,body=event).execute()

    def delete_event(self, eventId):
        return self.service().events().delete(calendarId=self.CALENDAR_ID, eventId=eventId).execute()