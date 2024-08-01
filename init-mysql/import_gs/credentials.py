__all__ = ['get_credentials']


import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


creds = None


def get_credentials(scopes):
    global creds
    if creds is not None:
        return creds
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    current_dir = Path(__file__).parent.resolve()
    token_json = current_dir / 'token.json'

    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(str(token_json), scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_json = current_dir.parent / 'credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_json), scopes
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_json, "w") as token:
            token.write(creds.to_json())

    return creds
