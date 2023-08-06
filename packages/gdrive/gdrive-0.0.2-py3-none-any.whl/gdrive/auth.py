import json
import logging
import os
import pickle
from typing import Type, TypeVar, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pykeepass import PyKeePass

from gdrive.exception import SettingsException

GA = TypeVar('GA', bound='GoogleAuth')
log = logging.getLogger(__name__)


class GoogleAuth:
    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    @classmethod
    def from_settings_file(cls: Type[GA], token_file: str, secrets_file: str, scopes: List[str]) -> GA:
        credentials = None
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(secrets_file, scopes)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
        return GoogleAuth(credentials)

    @classmethod
    def from_kdbx(cls: Type[GA], kdbx: PyKeePass, path: str, token_attachment: str, secrets_attachment: str,
                  scopes: List[str]) -> GA:
        credentials = None
        entry = kdbx.find_entries_by_path(path)
        token_attachments = [a for a in entry.attachments if a.filename == token_attachment]
        secrets_file = [a.data for a in entry.attachments if a.filename == secrets_attachment]
        if len(secrets_file) < 1:
            raise SettingsException(f"No KDBX attachments: {secrets_attachment} for: {path}")
        if len(secrets_file) > 1:
            raise SettingsException(f"Too many KDBX attachments for: {path}")

        if len(token_attachments) == 1:
            log.info("Token found in KDBX")
            credentials = pickle.loads(token_attachments[0].data)
        else:
            log.info(f"Cannot load token, number of matching attachments: {len(token_attachments)}")

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                config = json.loads(secrets_file[0])
                flow = InstalledAppFlow.from_client_config(config, scopes)
                credentials = flow.run_local_server(port=0)
            binary = pickle.dumps(credentials)
            bin_id = kdbx.add_binary(binary)
            # clear tokens and save new
            for token_attachment in token_attachments:
                entry.delete_attachment(token_attachment)
            entry.add_attachment(bin_id, token_attachment)
            kdbx.save()
            log.info(f"Updated KDBX: {path} entry")
        return GoogleAuth(credentials)
