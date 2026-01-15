from pymongo import MongoClient
import mimetypes
import pymongo
import hashlib
import pickle
import gridfs
import json
import os


class StoredFile:
    def __init__(self, path, load_content=True):
        if not os.path.isfile(path):
            raise FileNotFoundError(path)

        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(path)
        self.extension = os.path.splitext(path)[1].lstrip(".")
        self.mime_type = mimetypes.guess_type(path)[0]

        self.content = None
        self.hash = None

        if load_content:
            with open(path, "rb") as f:
                self.content = f.read()
            self.hash = hashlib.sha256(self.content).hexdigest()





def capsulize(data):
    data = pickle.dumps(json.dumps(data))
    return data

def decapsullize(data):
    data = pickle.loads(json.loads(data))
    return data