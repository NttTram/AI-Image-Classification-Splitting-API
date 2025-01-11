from fastapi import APIRouter, File, UploadFile
from services import image_service 

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)): 
    result = image_service.upload_image(file)
    return {"message: " : "Image uploaded successfully", "details: " : result}