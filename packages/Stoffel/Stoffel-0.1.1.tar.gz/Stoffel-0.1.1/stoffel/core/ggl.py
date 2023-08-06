#Import packages. 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
import pathlib
import pickle
import os
import io

from stoffel.core.utils.paths import path_leaf, gen_uuid
from stoffel.settings import *

class Slides:

    def __init__(self, presentation_id):
        self.slides = Google().slides()
        self.presentation_id = presentation_id
    
    def add_image(self, file_id, page_id, w, h, x, y):
        IMAGE_URL = f"https://drive.google.com/uc?export=view&id={file_id}"
        requests = []
        image_id = gen_uuid(1)
        requests.append({
            'createImage': {
                'objectId': image_id,
                'url': IMAGE_URL,
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': {
                            "magnitude" : h * 72, 
                            "unit" : "PT"
                        },
                        'width': {
                            "magnitude" : w * 72,
                            "unit" : "PT"
                        }
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": x * 72,
                        "translateY": y * 72,
                        "unit": "PT"
                    }
                }
            }
        })

        body = {
            'requests': requests
        }
        print(body)
        response = self.slides.presentations().batchUpdate(presentationId=self.presentation_id, body=body).execute()
        create_image_response = response.get('replies')[0].get('createImage')
        return create_image_response.get('objectId')

class Drive:

    def __init__(self, folder_id=None):
        self.drive = Google().drive()

    def create_folder(self, folder_name):
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder = self.drive.files().create(body=folder_metadata, fields="id").execute()
        return folder

    def create_image(self, file_path, parent=None):
        print(f"Creating image for {file_path}")
        file_name = path_leaf(file_path)
        file_metadata = {'name': file_name}
        if parent:
            file_metadata["parents"] = [parent]
        content = open(file_path, 'rb')
        media_body = MediaIoBaseUpload(content,'application/octet-stream', resumable=True)
        f = self.drive.files().create(
            body=file_metadata,
            media_body=media_body,
            fields='webViewLink, id'
        ).execute()
        return f

    def find_file(self, file_name):
        result = []
        page_token = None
        while True:
            response = self.drive.files().list(q=f"name contains '{file_name}' and trashed=false",
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token).execute()
            for file in response.get("files", []):
                result.append(file)
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
        return result

    def make_shareable(self, file_id):
        output = self.drive.permissions().create(
            fileId=file_id,
            body={
                "type" : "anyone", 
                "role" : "reader"
            },
            fields='id', 
        ).execute()
        return output

    def delete_file(self, file_id):
        return self.drive.files().delete(fileId=file_id).execute()

    def download_file(self, file_id, file_path, mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
        print(f"Downloading file {file_id} to {file_path}")
        request = self.drive.files().export_media(fileId=file_id, mimeType=mime_type)
        fh = io.FileIO(file_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

class Google:

    def __init__(self):
        self.creds_path = GOOGLE_CREDS_PATH
        self.token_path = GOOGLE_TOKEN_PATH
        self.scopes = GOOGLE_SCOPES
        self.redirect= GOOGLE_REDIRECT
        self.creds = self.credentials()

    def credentials(self):
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_path, scopes=self.scopes, redirect_uri=self.redirect)
                creds = flow.run_local_server(open_browser=True)
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def slides(self):
        service = build('slides', 'v1', credentials=self.creds, cache_discovery=False)  
        return service      

    def drive(self):
        service = build('drive', 'v3', credentials=self.creds, cache_discovery=False)  
        return service

if __name__=="__main__":
    #### ENV VARIABLES ####

    presentation_id = "1FJkzWBdb2AHL2-PKgu3BWFYtW9k1TK7OewTzvXX-BLI"
    slides = Slides(presentation_id)
    drive = Drive()
    folder = drive.create_folder("PantherTemp")
    print(drive.find_file("PantherTemp"))
    #directory = pathlib.Path(__file__).parent.parent.absolute()
    #f = drive.create_image(str(directory / "photos" / "test2_test_B3_D13.jpg"), parent=folder.get("id"))
    #print(drive.make_shareable(f.get("id")))
    #page_id = "g7d4b0c9081_0_22"
    #print(slides.add_image(f.get("id"), page_id))
    #print(drive.delete_file(f.get("id")))
    #sheet_id ="1Q1cm8MxDq0bzmok9PYzQc2ZjGSzNYRvjg5Yqggi_0f4"
    #drive.download_file(sheet_id)
