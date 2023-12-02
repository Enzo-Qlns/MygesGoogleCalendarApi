from services.utils import utils
from services.google import google
from services.myges import myges

from dotenv import load_dotenv
from dateutil import parser

import os
import argparse

load_dotenv()
utils = utils()
googleServices = google(CALENDAR_ID=os.getenv("CALENDAR_ID"))
mygesServices = myges(LOGIN=os.getenv("LOGIN"), PASSWORD=os.getenv("PASSWORD"))

def add_all_events():
    today_timestamp, one_year_later_timestamp = utils.get_today_and_one_year_later_timestamp_format()
    courses_myges = mygesServices.get_agenda(
        start=today_timestamp,
        end=one_year_later_timestamp
    )
    
    for course in courses_myges:
        teacher = course['discipline']['teacher']
        summary = course['name']
        start_date = course['start_date'] / 1000
        end_date = course['end_date'] / 1000
        googleServices.create_event(
            summary=summary,
            description=teacher,
            startDate=utils.convert_unix_timestamp_to_iso(start_date),
            endDate=utils.convert_unix_timestamp_to_iso(end_date),
        )

def delete_all_events():
    google_events = googleServices.get_events_from_today()
    for event in google_events:
        googleServices.delete_event(eventId=utils.decode_google_event_eid(htmlLink=event['htmlLink']))

def update_all_events():
    google_events = googleServices.get_events_from_today()
    today_timestamp, one_year_later_timestamp = utils.get_today_and_one_year_later_timestamp_format()
    courses_myges = mygesServices.get_agenda(
        start=today_timestamp,
        end=one_year_later_timestamp
    )
    
    array_event_start_date = [parser.parse(event['start']['dateTime']).strftime('%Y-%m-%dT%H:%M:%S') for event in google_events]
    array_event_end_date = [parser.parse(event['end']['dateTime']).strftime('%Y-%m-%dT%H:%M:%S') for event in google_events]

    for course in courses_myges:
        start_date = utils.convert_unix_timestamp_to_iso(course['start_date']/1000)
        end_date = utils.convert_unix_timestamp_to_iso(course['end_date']/1000)
        if start_date in array_event_start_date and end_date in array_event_end_date:
            current_index = array_event_start_date.index(start_date)
            updated_teacher = 'NC' if course['discipline']['teacher'] == ' ' else course['discipline']['teacher']
            updated_summary = course['name']
            updated_start_date = utils.convert_unix_timestamp_to_iso(course['start_date']/1000) + '.000Z'
            updated_end_date = utils.convert_unix_timestamp_to_iso(course['end_date']/1000) + '.000Z'
            googleServices.update_event(
                eventId=utils.decode_google_event_eid(htmlLink=google_events[current_index]['htmlLink']),
                summary=updated_summary,
                startDate=updated_start_date,
                endDate=updated_end_date,
                description=updated_teacher
            )
            
def main():
    parser = argparse.ArgumentParser(description='Perform actions on events.')
    parser.add_argument('--add-all', action='store_true', help='Add all events')
    parser.add_argument('--del-all', action='store_true', help='Delete all events')
    parser.add_argument('--update-all', action='store_true', help='Update all events')

    args = parser.parse_args()

    if args.add_all:
        add_all_events()
    elif args.del_all:
        delete_all_events()
    elif args.update_all:
        update_all_events()
    
if __name__ == '__main__':
    main()