
from __future__ import print_function
from pypresence import Presence

import time
import datetime
import pickle
import os.path
import json
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None

    while True: 

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
        tz = pytz.timezone('US/Central')
        # Call the Calendar API
        now = datetime.datetime.utcnow()# 'Z' indicates UTC time
        timeChange = datetime.timedelta(minutes = 15)
        now2 = now + timeChange
     
      
        body = {
            "timeMin": now.isoformat() + "Z",
            "timeMax": now2.isoformat() + "Z",
            "timeZone": 'US/Central',
            "items": [{"id": 'email@gmail.com'}]
        }
        events_result = service.freebusy().query(body=body).execute()
        events = events_result

        if(events['calendars'].get('email@gmail.com').get('busy') != None):
            client_id = "" #busy 
            
            RPC = Presence(client_id)  # Initialize the Presence client

            RPC.connect() # Start the handshake loop

            RPC.update(state="Rich Presence using pypresence!") # Updates our presence

        else:
            client_id = ""  # online   
            RPC = Presence(client_id)  # Initialize the Presence client

            RPC.connect() # Start the handshake loop

            RPC.update(state="Rich Presence using pypresence!") # Updates our presence

            
       


        time.sleep(3000);


if __name__ == '__main__':
    main()