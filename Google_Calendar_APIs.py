import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from Database_manager import Database
import datetime

Calendar_Study_ID='24assm5qtgmicvl5be11k97gf0@group.calendar.google.com'

def Connect_Service():
    CLIENT_SECRET_FILE = 'client_secrect.json'
    API_SERVICE_NAME = "calendar"
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
    print(SCOPES)

    cred = None
    working_dir = os.getcwd()
    token_dir = 'token files'

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
        with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, pickle_file))
        return  None

def Add_Event(db: Database, Name: str, Date: str, Start_Time: str, End_Time: str, ID: str):
    service = Connect_Service()

    event = {
      'summary': Name,
      'start': {
        'dateTime': f'{Date}T{Start_Time}:00+07:00',
        'timeZone': 'Asia/Ho_Chi_Minh',
      },
      'end': {
        'dateTime': f'{Date}T{End_Time}:00+07:00',
        'timeZone': 'Asia/Ho_Chi_Minh',
      }
    }
    event = service.events().insert(calendarId=Calendar_Study_ID, body=event).execute()
    id_event = event.get('id')
    print(f"Event with ID {id_event} created: {event.get('htmlLink')}")

def get_list_event():
    service = Connect_Service()
    previous_date = str(datetime.date.today() - datetime.timedelta(days=2))
    timeMin = f'{previous_date}T00:00:00+07:00'
    ls_event_id = list()
    page_token = None
    while True:
      events = service.events().list(calendarId=Calendar_Study_ID, timeMin=timeMin, pageToken=page_token).execute()
      for event in events['items']:
        ls_event_id.append(event['id'])
        # print(f"{event['id']} - {type(event['id'])}")
      page_token = events.get('nextPageToken')
      if not page_token:
        break
    return ls_event_id

def Update_event(Date: str, Start_Time: str, End_Time: str, ID_event: str):
    service = Connect_Service()
    event = service.events().get(calendarId=Calendar_Study_ID, eventId=ID_event).execute()
    event['start']['datetime'] = f'{Date}T{Start_Time}:00+07:00'
    event['end']['datetime'] = f'{Date}T{End_Time}:00+07:00'
    updated_event = service.events().update(calendarId=Calendar_Study_ID, eventId=ID_event, body=event).execute()
    print('Event updated %s' % (updated_event.get('htmlLink')))

'''
#Print list of Calendar
service =  Connect_Service()
response = service.calendarList().list().execute()
print(response.keys())
for item in response.get('items'):
    print(item)

2011-06-03T00:00:00+07:00

'''