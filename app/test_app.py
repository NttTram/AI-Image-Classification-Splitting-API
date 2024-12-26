from fastapi import FastAPI
from fastapi import UploadFile, File
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    return {"info": "File received"}

