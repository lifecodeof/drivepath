from typing import cast
from pydrive2.files import GoogleDriveFile

from drivepath.drive import Drive
from drivepath.exceptions import PathNotFoundException
from drivepath.metadata_types import GoogleDriveFileMetadata
from drivepath.query import Expression, q


class DrivePath:
    _drive: Drive
    _obj: GoogleDriveFile

    def __init__(self, drive: Drive, file_object: GoogleDriveFile):
        self._drive = drive
        self._obj = file_object

    def _make_path(self, _obj: GoogleDriveFile):
        return DrivePath(self._drive, _obj)

    @property
    def metadata(self) -> GoogleDriveFileMetadata:
        if self._obj.metadata is None or len(self._obj.metadata) == 0:
            self._obj.FetchMetadata(fetch_all=True)

        return cast(GoogleDriveFileMetadata, self._obj.metadata)

    def iterdir(self):
        for file in self._obj:
            yield self._make_path(file)

    def query(self, query: Expression):
        """Executes a query on direct children of this path"""
        return (q(self.id, "in", "parents") & query).execute(self._drive)

    def get_child(self, child_title: str):
        try:
            return next(self.query(q("title", "=", child_title)))
        except StopIteration:
            raise PathNotFoundException(self, child_title)

    def __truediv__(self, other: str):
        return self.get_child(other)

    def __repr__(self):
        return f"DrivePath(id={self.id}, title='{self.title}')"

    def create_file(self, title: str, content: str | None = None):
        return self._drive.create_file(self.id, title, content)

    def create_folder(self, title: str):
        return self._drive.create_folder(self.id, title)

    def mkdirp(self, *parts: str):
        """Create a folder recursively if it does not exist. Similar to `mkdir -p`"""
        current_path: DrivePath = self
        created_folder = False
        for part in parts:
            if created_folder:
                current_path = current_path.create_folder(part)
            else:
                try:
                    current_path = current_path.get_child(part)
                except PathNotFoundException:
                    current_path = current_path.create_folder(part)
                    created_folder = True

        return current_path

    # Frequently used metadata properties
    @property
    def id(self) -> str:
        return self.metadata["id"]

    @property
    def title(self) -> str:
        return self.metadata["title"]
