from fastapi import APIRouter, UploadFile, File
router = APIRouter()

@router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename" : file.filename}

#

