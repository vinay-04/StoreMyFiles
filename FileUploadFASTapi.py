import pyrebase as pb
import json
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
import uvicorn
import os


with open('config.json') as data:
    config = json.load(data)


app = FastAPI(title="File Upload")

class CloudStorage:
    def __init__(self, cred):
        self.apiKey = cred['apiKey']
        self.authDomain = cred['authDomain']
        self.projectId = cred['projectId']
        self.storageBucket = cred['storageBucket']
        self.messagingSenderId = cred['messagingSenderId']
        self.appId = cred['appId']
        self.measurementId = cred['measurementId']
        self.databaseURL = cred['databaseURL']
        self.firebase = pb.initialize_app(cred)
    
    def initializeFirebaseStorage(self):
        self.storage = self.firebase.storage()

    def uploadFile(self):
        try:
            @app.post('/file-upload')
            async def uploadFile(file:UploadFile = File(...)):
                contents = file.file.read()
                os.system(f"touch uploads/{file.filename}")
                with open(f"uploads/{file.filename}", "wb") as f:
                    f.write(contents)
                    file.file.close()
                self.file_type = file.filename.split('.').pop()
                self.file_name = file.filename[:-len(self.file_type)-1]
                self.storage.child(f"uploads/{file.filename}").put(f"uploads/{file.filename}")
                os.system(f"rm uploads/{file.filename}")
                return {"fileName":self.file_name, "fileType":self.file_type}
        except Exception:
            return HTTPException

c1 = CloudStorage(config)
c1.initializeFirebaseStorage()

c1.uploadFile()


if __name__ == '__main__':
    uvicorn.run("FileUploadFASTapi:app",reload=True)