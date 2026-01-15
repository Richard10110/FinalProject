from pymongo import MongoClient
import mimetypes
import pymongo
import hashlib
import pickle
import gridfs
import json
import os


class file_information:

    def __init__(self,file_name):
        with open(file_name,"rb") as f:
            content = f.read()
        self.cont = content
        self.name = file_name
        self.size = os.path.getsize(file_name)
        self.format = file_name.split(".")[-1]
        self.type = mimetypes.guess_type(f"{file_name}")[0]
        self.hash = hashlib.sha256(self.cont).hexdigest()

    def file_content(self):
        return self.cont

    def get_meta(self):
        metadata = {
            "file_name": self.name,
            "size": self.size,
            "format": self.format,
            "type": self.type,
        }
        return metadata

    def get_pickled(self):
        data = self.get_meta()
        data = json.dumps(data)
        data = pickle.dumps(data)
        return data


    # def mongo_connect_upload(self):


# this part will work in the server side
#              |   |   |
#              |   |   |
#              V   V   V
# optional to make a hash equation with files binary sha256, keep it in mind.
class mongo:
    def __init__(self):
        self.client = "mongodb+srv://richi_user:1234@cluster0.ghruhmw.mongodb.net/?appName=Cluster0"
        self.data = "Files_DataBase"
        self.collection = "files_collection"


    def upload_file(self,metadata,file_content):

        metadata = pickle.loads(metadata)
        metadata = json.loads(metadata)

        cli = MongoClient(self.client)
        db = cli[self.data]
        collection = db[self.collection]
        fs = gridfs.GridFS(db)

        file_id = fs.put(
            file_content,  # bytes
            filename=metadata["file_name"],# --> file name added
            metadata=metadata
        )
        print(file_id,"Uploaded!")


    def del_file(self,filename):
        cli = MongoClient(self.client)
        db = cli[self.data]
        collection = db[self.collection]
        fs = gridfs.GridFS(db)

        file_doc = fs.get_last_version(filename)
        fs.delete(file_doc._id)
        print("Deleted successfully!",file_doc._id)


    def download_file(self,filename):
        cli = MongoClient(self.client)
        db = cli[self.data]
        collection = db[self.collection]
        fs = gridfs.GridFS(db)

        try:

            grid_out = fs.get_last_version(filename)

            return grid_out,grid_out.length
            # with open("downloaded_" + filename, "wb") as f:
            #     f.write(grid_out.read())

        except:
            print("Invalid file")





def transfer_bytes(space):
    if space > 1000 and space < 1000000:
        space = f"{space / 1000} KB"
    elif space > 1000000 and space < 1000000000:
        space = f"{space / 1000000} MB"
    elif space > 1000000000:
        space = f"{space} GB"

    return space

