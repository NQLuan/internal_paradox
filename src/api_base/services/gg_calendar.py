#!/usr/bin/env python

# author Huy
# date 11/25/2019

import datetime
import os.path
import pickle

from django.conf import settings
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleCalendar:
    # If modifying these scopes, delete the file token.pickle.

    @staticmethod
    def get_calendar_service():
        scopes = ['https://www.googleapis.com/auth/calendar']

        credentials_file = 'api/credentials.json'
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        return service

    @staticmethod
    def create_event(data, user_team):
        title = f"{data.get('title')} - {user_team} - {data.get('content')}"
        reason = 'No reason'
        if data.get('reason'):
            reason = data.get('reason')
        start = str(data.get('date')) + 'T' + data.get('content').split(' ')[-3][1:6] + ':00'
        end = str(data.get('date')) + 'T' + data.get('content').split(' ')[-1][:5] + ':00'
        service = GoogleCalendar.get_calendar_service()
        service.events().insert(
            calendarId=settings.CALENDAR_ID,
            body={
                "summary": title,
                "description": f'Reason: {reason}',
                "start": {"dateTime": start, "timeZone": 'Asia/Ho_Chi_Minh'},
                "end": {"dateTime": end, "timeZone": 'Asia/Ho_Chi_Minh'},
            },
        ).execute()
        return False

    @staticmethod
    def get():
        service = GoogleCalendar.get_calendar_service()
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId=settings.CALENDAR_ID, timeMin=now,
            maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    @staticmethod
    def update_event(data, old_content, new_content, user_team):
        # update the event to according time
        service = GoogleCalendar.get_calendar_service()
        title = f"{data.get('title')} - {user_team} - {new_content}"
        reason = 'No reason'
        if data.get('reason'):
            reason = data.get('reason')
        start = str(data.get('date')) + 'T' + new_content.split(' ')[-3][1:6] + ':00'
        end = str(data.get('date')) + 'T' + new_content.split(' ')[-1][:5] + ':00'

        calendar_id = None
        items = GoogleCalendar.get()
        for item in items:
            if item.get('summary') == f"{data.get('title')} - {user_team} - {old_content}" and item.get('start').get(
                    'dateTime')[:10] == data.get('start'):
                calendar_id = item.get('id')
        if calendar_id:
            service.events().update(
                calendarId=settings.CALENDAR_ID,
                eventId=calendar_id,
                body={
                    "summary": title,
                    "description": f'Reason: {reason}',
                    "start": {"dateTime": start, "timeZone": 'Asia/Ho_Chi_Minh'},
                    "end": {"dateTime": end, "timeZone": 'Asia/Ho_Chi_Minh'},
                },
            ).execute()

    @staticmethod
    def delete_event(items, dates, user_team):
        service = GoogleCalendar.get_calendar_service()
        try:
            calendar_id = None
            for date in dates:
                for item in items:
                    if item.get('summary') == f"{date.title} - {user_team} - {date.content}" and item.get('start').get(
                            'dateTime')[:10] == str(date.date):
                        calendar_id = item.get('id')
                if calendar_id:
                    service.events().delete(
                        calendarId=settings.CALENDAR_ID,
                        eventId=calendar_id,
                    ).execute()
                    calendar_id = None
        except:
            raise Exception("Failed to delete event")
