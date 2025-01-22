import os
from app.models.image_model import ImageModel
from fastapi import UploadFile, HTTPException, File


img_formats = ('.png', 'jpg', 'jpeg')

img_dir = "app/data/img"
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

## upload_image():
## 1. Upload a file and save it to img_dir [Done]
## 2. Make sure the file uploaded is image format compatible [Done]
def upload_image(file: UploadFile):
    try:
        
        # Check file format
        if not file.filename.lower().endswith(img_formats):
            raise HTTPException(status_code=415, detail="Unsupported file format. Only 'jpg', 'jpeg', and 'png' are allowed.")
            
        # # # Check file size
        # if file.content_length > 10000000:
        #     raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
            
        file_name = os.path.splitext(file.filename)[0]
        
        # Check if file already exists
        if os.path.exists(os.path.join(img_dir, file_name)):
            raise HTTPException(status_code=409, detail="File already exists.")
            
        # Save the uploaded file in the specified location (img_dir)
        ## Create the directory based on the uploaded file name
        file_location = f"{img_dir}/{file_name}"
        if not os.path.exists(file_location):
            os.makedirs(file_location)
        
        # ## Write in binary mode with read/write permissions
        # with open(file_location, "wb+") as file_object:
        #     file_object.write(file.file.read())
            
        # Create an instance of ImageModel to return
        image_data = ImageModel(name=file.filename, description="Uploaded image")
            
        return image_data.dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    


def upload_file(file: UploadFile):
    file_location = os.path.join(img_dir, file.filename)

    # Save the uploaded file
    try:
        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
## list_processed_image():
## 1. Show all the images from the latest image uploaded through the POST /upload/
## 2. If no images then return empty + message to ask user to upload images through POST /upload, 'jpeg'/
# def get_latest_uploaded_images():
#     images = list_images()
#     # if returned type if dictionary, it means there are no images
#     if isinstance(images, dict):
#         return images
#     # Assuming 
#     latest_images = sorted(images, key=lambda x: os.path.getmtime(x, reverse=True))
    
#     return latest_images


## list_images():
## 1. List all the images stored in app/data/img [Done]
## 2. If empty prompt user to start uploading images through POST /upload/ [Done]
def list_images():

    images = []
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            if file.lower().endswith(img_formats):
                images.append(os.path.join(root, file))
    if not images:
        return {"message" : "No images found. Please upload image through POST /v1/upload/"}
    return images