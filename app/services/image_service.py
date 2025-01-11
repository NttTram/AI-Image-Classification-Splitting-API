import os
from models.image_model import ImageModel
from fastapi import UploadFile, HTTPException

img_dir = "app/data/img"
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

## process_upload():
## 1. Upload a file and save it to img_dir [Done]
## 2. Make sure the file uploaded is image format compatible
def process_upload(file: UploadFile):
    try:
        
        ## Create the directory based on the uploaded file name
        file_location = f"{img_dir}/{file.filename}"
        if not os.path.exists(file_location):
            os.makedirs(file_location)
        
        ## Write in binary mode with read/write permissions
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
            
            
        return {"Filename: " : file.filename, "location: " : file.location}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    
    