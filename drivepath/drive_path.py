from typing import cast
from pydrive2.files import GoogleDriveFile

from drivepath.metadata_types import GoogleDriveFileMetadata


class DrivePath:
    _obj: GoogleDriveFile

    def __init__(self, file_object: GoogleDriveFile) -> None:
        self._obj = file_object

    @property
    def metadata(self) -> GoogleDriveFileMetadata:
        if self._obj.metadata is None or len(self._obj.metadata) == 0:
            self._obj.FetchMetadata(fetch_all=True)

        return cast(GoogleDriveFileMetadata, self._obj.metadata)

    def iterdir(self):
        for file in self._obj:
            yield DrivePath(file)
