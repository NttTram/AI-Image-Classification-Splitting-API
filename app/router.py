from fastapi import APIRouter, UploadFile, File
import uuid
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
import cv2
router = APIRouter()


# Load the pre-trained model
model_dir = tf.saved_model.load('/app/data/modelset/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model/')
model = tf.saved_model.load(model_dir)



@router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename" : file.filename}




@router.post("/detect/")
# async def detect_image(file: UploadFile = File(...)):
#     # Check file type
#     if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
#         return JSONResponse(status_code=400, content={"message" : "Invalid file format"})
    
#     # Save file to a secure location
#     file_location = f"/app/data/img/{str(uuid.uuid4())}-{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         file_object.write(await file.read())
        
#     # Perform image detection, recognition, and segmentation
#     results = process_image(file_location) # Placeholder for the actual processing function
    
#     return results

async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Prepare the image for the model
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_img = cv2.resize(img, (320, 320))
    input_tensor = tf.convert_to_tensor([resized_img], dtype=tf.float32)
    
    # Inference
    infer = model.signatures['serving_default']
    outputs = infer(input_tensor)
    
    # Process outputs
    
    return {"message" : "Image processed successfully"}

def process_image(image_path):
    # Implement image processing logic here
    # For example, use a pre-trained model to detect objects, classify objects, and segment the image
    # Return the detected objects, classifications, and segmentation results
    return {"status": "success", "data" : "Processed image details would be here"}


