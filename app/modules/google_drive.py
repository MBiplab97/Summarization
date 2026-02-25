from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import io

class GoogleDriveService:

    async def list_files(self, folder_id: str):
        # OAuth2 authentication
        # Hardcoded folder_id allowed as per assignment
        service = build("drive", "v3", credentials=self._get_credentials())

        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="files(id, name, mimeType)"
        ).execute()

        return results.get("files", [])

    async def download_file(self, file):
        service = build("drive", "v3", credentials=self._get_credentials())
        request = service.files().get_media(fileId=file["id"])
        file_data = io.BytesIO(request.execute())
        return file_data

    def _get_credentials(self):
        return Credentials.from_service_account_file(
            "credentials.json",
            scopes=["https://www.googleapis.com/auth/drive"]
        )