import json
from drivepath.drive import Drive


def test_metadata():
    new_var = Drive.from_local_auth()
    new_var1 = new_var.get_root()
    m = new_var1.metadata
    print(json.dumps(m))
