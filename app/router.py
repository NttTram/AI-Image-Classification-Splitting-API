from fastapi import APIRouter
from fastapi import UploadFile, File, UploadFile

router = APIRouter()

@router.post("/upload/")

async def create_upload_file(file: UploadFile = File(...)):
    return {"filename" : file.filename}


