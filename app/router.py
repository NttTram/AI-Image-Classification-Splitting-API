from fastapi import APIRouter
from fastapi import UploadFile, File
router = APIRouter()

@router.post("/upload/")

# async def create_upload_file(file: UploadFile = File(...)):
#     return {"filename" : file.filename}


async def create_upload_file(file: UploadFile = File(...)):
    return {"info": "File received"}


