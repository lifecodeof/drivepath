from drivepath.drive_path import DrivePath


class PathNotFoundException(Exception):
    source: DrivePath
    child_title: str

    def __init__(self, source: DrivePath, child_title: str):
        self.source = source
        self.child_title = child_title
        super().__init__(f"Path '{child_title}' not found in '{source.title}'")
