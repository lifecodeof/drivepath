import os
from typing import Iterator, Self
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
from pydrive2.files import GoogleDriveFile

from drivepath.drive_path import DrivePath
from drivepath.query import Expression


class Drive:
    _drive: GoogleDrive

    def __init__(self, drive: GoogleDrive):
        self._drive = drive

    @classmethod
    def from_credentials_file(cls, credentials_path: str) -> Self:
        auth = GoogleAuth()
        auth.LoadCredentialsFile(credentials_path)
        return cls(GoogleDrive(auth))

    @classmethod
    def from_local_auth(cls, credentials_path: str = "credentials.json") -> Self:
        """
        Create a Drive instance using the local webserver auth method with credentials remembered.
        """

        auth = GoogleAuth()

        if os.path.exists(credentials_path):
            auth.LoadCredentialsFile(credentials_path)

        if not auth.credentials or auth.access_token_expired:
            auth.LocalWebserverAuth()
            auth.SaveCredentialsFile(credentials_path)

        return cls(GoogleDrive(auth))

    def save_credentials(self, credentials_path: str) -> None:
        auth = self._drive.auth
        if auth is None:
            raise ValueError("Drive instance does not have an auth.")

        auth.SaveCredentialsFile(credentials_path)

    def get_path(self, file_id: str) -> DrivePath:
        file_obj = self._drive.CreateFile({"id": file_id})
        return self._make_path(file_obj)

    def get_root(self) -> DrivePath:
        return self.get_path("root")

    def query(self, query: str | Expression) -> Iterator[DrivePath]:
        iterator = self._drive.ListFile({"q": str(query)}).GetList()
        return map(self._make_path, iterator)

    def _make_path(self, file_obj: GoogleDriveFile) -> DrivePath:
        return DrivePath(self, file_obj)

    def create_file(self, parent_id: str, title: str, content: str | None = None):
        file = self._drive.CreateFile({"title": title, "parents": [{"id": parent_id}]})
        if content:
            file.SetContentString(content)
        file.Upload()
        return self._make_path(file)

    def create_folder(self, parent_id: str, title: str):
        folder = self._drive.CreateFile(
            {"title": title, "parents": [{"id": parent_id}], "mimeType": "application/vnd.google-apps.folder"}
        )
        folder.Upload()
        return self._make_path(folder)
