from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

def upload_to_drive(filename, stream_data):
    creds = Credentials.from_authorized_user_file('client_secrets.json', ['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)

    media = MediaIoBaseUpload(io.BytesIO(stream_data.read()), mimetype='application/octet-stream', resumable=True)
    file_metadata = {'name': filename}
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
