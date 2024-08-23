from typing import Iterator, Self
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
from pydrive2.files import GoogleDriveFile

from drivepath.drive_path import DrivePath


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

    def get_file(self, file_id: str) -> DrivePath:
        file_obj = self._drive.CreateFile({'id': file_id})
        return DrivePath(file_obj)

    def get_root(self) -> DrivePath:
        return DrivePath(self._drive.CreateFile({'id': 'root'}))

    def query(self, query: str) -> Iterator[DrivePath]:
        iterator =  self._drive.ListFile({'q': query}).GetList()
        return map(DrivePath, iterator)
