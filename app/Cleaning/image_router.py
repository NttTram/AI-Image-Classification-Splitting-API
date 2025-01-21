from fastapi import APIRouter, File, UploadFile
from app.services.image_service import list_images, upload_file, upload_image

router = APIRouter()

@router.post("/upload/")
async def upload(file: UploadFile = File(...)): 
    result = upload_image(file)
    return {"filename": result["name"],}


@router.get("/images/")
async def list_images():
    images = list_images()
    return {"images": images}
