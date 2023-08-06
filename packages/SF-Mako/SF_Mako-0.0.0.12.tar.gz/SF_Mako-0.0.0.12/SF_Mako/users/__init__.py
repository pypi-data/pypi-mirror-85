import bcrypt
import base64
from essentials import tokening
import time
from .. import filing
import os
import datetime
import json

os.makedirs("mako_data", exist_ok=True)
os.makedirs("mako_data/devices", exist_ok=True)
all_DIDs = filing.Updating_Dict_File("mako_data/devices/did.ls")

date_format = "%y_%m_%d"
time_format = "%H_%M_%S"


def __compress_creds__(auth):
    return base64.encodebytes(auth).decode()

def __decompress_creds__(auth):
    return base64.decodebytes(auth.encode())

def __slice_n_dice__(self, auth):
    auth = auth.encode()
    hashed = bcrypt.hashpw(auth, bcrypt.gensalt())
    if bcrypt.checkpw(auth, hashed):
        return hashed
    else:
        raise ValueError("Hashing Failed.")

def create_user(username, password, meta=None):
    user = User_object()


class User_Device:

    def __init__(self, DID=None, IP=None):
        self.IP = IP
        if DID is None:
            self.DID = tokening.CreateToken(30, all_DIDs)
            all_DIDs[self.DID] = datetime.datetime.now().timestamp()
        else:
            self.DID = DID
        os.makedirs(f"mako_data/devices/{self.DID}", exist_ok=True)
        self.Log = filing.Appender_File(f"mako_data/devices/{self.DID}/{datetime.datetime.now().strftime(date_format)}")

    def new_log_entry(self, entry, IP=None, date=None):
        if date is None:
            date = datetime.datetime.now().strftime(date_format)
        if IP is not None:
            self.IP = IP
        self.Log.append(json.dumps({"entry": entry, "ip": self.IP, "date": date, "time": datetime.datetime.now().strftime(time_format)}))

class User_Session:

    def __init__(self):
        pass



class User_object:

    def __init__(self, username, verified=False, meta=None):
        pass
