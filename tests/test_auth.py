import os
from drivepath.drive import Drive


def test_save_credentials():
    Drive.from_local_auth()

    # disable user interaction to assert that the saved credentials are used
    os.environ["GDRIVE_NON_INTERACTIVE"] = "True"
    Drive.from_local_auth()
