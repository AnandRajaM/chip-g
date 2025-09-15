from datetime import datetime, timezone
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]





def get_calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
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
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None





def get_upcoming_events(service, max_results=10):
    try:
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []



#   try:
#     service = build("calendar", "v3", credentials=creds)

#     # Call the Calendar API
#     now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
#     print("Getting the upcoming 10 events")
#     events_result = (
#         service.events()
#         .list(
#             calendarId="primary",
#             timeMin=now,
#             maxResults=10,
#             singleEvents=True,
#             orderBy="startTime",
#         )
#         .execute()
#     )
#     events = events_result.get("items", [])

#     if not events:
#       print("No upcoming events found.")
#       return

#     # Prints the start and name of the next 10 events
#     for event in events:
#       start = event["start"].get("dateTime", event["start"].get("date"))
#       print(start, event["summary"])

#   except HttpError as error:
#     print(f"An error occurred: {error}")







def getCalendarList( service ):
  calendarList = service.calendarList()
  print( calendarList )
  calendarListResult = calendarList.list().execute()
  print( calendarListResult )
  print("done?")

  


def createEvent(service):  
    local_tz = pytz.timezone('Asia/Kolkata')  
    local_time = datetime.now(local_tz)
    
    print("Local time:", local_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
    
    start_time = local_time + timedelta(minutes=2)
    end_time = start_time + timedelta(minutes=2)
    
    event = {
        'summary': 'Test Event',
        'location': 'Online',
        'description': 'Yo it workz?? sick! :)',
        'start': {
            'dateTime': start_time.isoformat(),  
            'timeZone': str(local_tz),
        },
        'end': {
            'dateTime': end_time.isoformat(),  
            'timeZone': str(local_tz),
        },
        'reminders': {
            'useDefault': True,
        },
    }
    
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))




if __name__ == "__main__":
    service = get_calendar_service()
    # events = get_upcoming_events(service, 20)
    # if not events:
    #     print("No upcoming events found.")
    # for event in events:
    #     start = event["start"].get("dateTime", event["start"].get("date"))
    #     print(start, event["summary"])

    # getCalendarList( service )
    createEvent( service )