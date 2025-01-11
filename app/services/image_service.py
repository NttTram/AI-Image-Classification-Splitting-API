import os
from models.image_model import ImageModel
from fastapi import UploadFile, HTTPException


img_formats = ('.png', 'jpg', 'jpeg')

img_dir = "app/data/img"
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

## upload_image():
## 1. Upload a file and save it to img_dir [Done]
## 2. Make sure the file uploaded is image format compatible
def upload_image(file: UploadFile):
    try:
        
        # Check file format
        if not file.filename.lower().endswith(img_formats):
            raise HTTPException(status_code=415, detail="Unsupported file format. Only 'jpg', 'jpeg', and 'png' are allowed.")
            
        # Check file size
        if file.content_length > 10000000:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
            
        # Check if file already exists
        if os.path.exists(os.path.join(img_dir, file.filename)):
            raise HTTPException(status_code=409, detail="File already exists.")
            
        # Save the uploaded file in the specified location (img_dir)
         
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
    
    
    
## list_processed_image():
## 1. Show all the images from the latest image uploaded through the POST /upload/
## 2. If no images then return empty + message to ask user to upload images through POST /upload, 'jpeg'/



## list_images():
## 1. List all the images stored in app/data/img
## 2. If empty prompt user to start uploading images through POST /upload/
def list_images():
    images = []
    for root, dirs, files in os.walk(img_dir):
        for file in  files:
            if file.lower().endswith(img_formats):
                images.append(os.path.join(root, file))
    return images