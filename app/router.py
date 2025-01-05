from fastapi import APIRouter, UploadFile, File, Response
import uuid
from fastapi.responses import JSONResponse
import os
import tensorflow as tf
import numpy as np
import cv2
router = APIRouter()


# Load the pre-trained model
model_dir = '/app/data/modelset/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model'
print("Loading model from:", model_dir)
print("Is path correct?", os.path.exists(model_dir))

model = tf.saved_model.load(model_dir)




@router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename" : file.filename}



def draw_detections(image, boxes, classes, scores, class_names):
    for i, box in enumerate(boxes):
        if scores[i] >= 0.2:
                 
            class_id = int(classes[i])  # Convert class ID to integer
            label = class_names.get(class_id, f"Unlabeled (ID {class_id})")  # Default to Unlabeled
          
            # Ensure boxes are scaled back to the original image size
            y_min, x_min, y_max, x_max = boxes[i]
            x_min = int(x_min * image.shape[1])
            x_max = int(x_max * image.shape[1])
            
            y_min = int(y_min * image.shape[0])
            y_max = int(y_max * image.shape[0])

            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            cv2.putText(image, label, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return image

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
    input_tensor = tf.convert_to_tensor([resized_img], dtype=tf.uint8)
    
    
    print(model.signatures['serving_default'].inputs)
    print("Shape of input tensor:", input_tensor.shape)
    print("Data type of input tensor:", input_tensor.dtype)

    # Inference
    infer = model.signatures['serving_default']
    
    # Run detections
    outputs = infer(input_tensor)
   
    
    # Extracting outputs
    detection_boxes = outputs['detection_boxes'].numpy()[0]   # [1, num_detections, 4]
    detection_classes = outputs['detection_classes'].numpy()[0].astype(int)  # [1, num_detections]
    detection_scores = outputs['detection_scores'].numpy()[0]  # [1, num_detections]
    
    class_names = {
        1: "Person",
        2: "Bicycle",
        3: "Car",
        4: "Motorcycle",
        5: "Airplane",
        6: "Bus",
        7: "Train",
        8: "Truck",
        9: "Boat",
        10: "Traffic Light",
        11: "Fire Hydrant",
        12: "Unknown",  # not used
        13: "Stop Sign",
        14: "Parking Meter",
        15: "Bench",
        16: "Bird",
        17: "Cat",
        18: "Dog",
        19: "Horse",
        20: "Sheep",
        21: "Cow",
        22: "Elephant",
        23: "Bear",
        24: "Zebra",
        25: "Giraffe",
        26: "Unknown",  # not used
        27: "Backpack",
        28: "Umbrella",
        29: "Unknown",  # not used
        30: "Unknown",  # not used
        31: "Handbag",
        32: "Tie",
        33: "Suitcase",
        34: "Frisbee",
        35: "Skis",
        36: "Snowboard",
        37: "Sports Ball",
        38: "Kite",
        39: "Baseball Bat",
        40: "Baseball Glove",
        41: "Skateboard",
        42: "Surfboard",
        43: "Tennis Racket",
        44: "Bottle",
        45: "Unknown",  # not used
        46: "Wine Glass",
        47: "Cup",
        48: "Fork",
        49: "Knife",
        50: "Spoon",
        51: "Bowl",
        52: "Banana",
        53: "Apple",
        54: "Sandwich",
        55: "Orange",
        56: "Broccoli",
        57: "Carrot",
        58: "Hot Dog",
        59: "Pizza",
        60: "Donut",
        61: "Cake",
        62: "Chair",
        63: "Couch",
        64: "Potted Plant",
        65: "Bed",
        66: "Unknown",  # not used
        67: "Dining Table",
        68: "Unknown",  # not used
        69: "Unknown",  # not used
        70: "Toilet",
        71: "Unknown",  # not used
        72: "TV",
        73: "Laptop",
        74: "Mouse",
        75: "Remote",
        76: "Keyboard",
        77: "Cell Phone",
        78: "Microwave",
        79: "Oven",
        80: "Toaster",
        81: "Sink",
        82: "Refrigerator",
        83: "Unknown",  # not used
        84: "Book",
        85: "Clock",
        86: "Vase",
        87: "Scissors",
        88: "Teddy Bear",
        89: "Hair Drier",
        90: "Toothbrush"
    }
  

    
    processed_image = draw_detections(
        image, detection_boxes, detection_classes, detection_scores, class_names
    )
    
    # Convert the image to JPEG format before sending the response
    _, encoded_image = cv2.imencode('.jpg', processed_image)

    return Response(content=encoded_image.tobytes(), media_type='image/jpeg')
    # return process_output(detection_boxes, detection_classes, detection_scores, image.shape)

def process_output(boxes, classes, scores, image_shape):
    H, W = image_shape[0], image_shape[1]
    results = []

    for i in range(len(scores)):
        if scores[i] >= 0.5:  # threshold can be adjusted based on needs
            y_min, x_min, y_max, x_max = boxes[i]
            (left, right, top, bottom) = (x_min * W, x_max * W, y_min * H, y_max * H)
            results.append({
                "class_id": int(classes[i]),
                "score": float(scores[i]),
                "bbox": [int(left), int(top), int(right), int(bottom)]
            })

    return {"detections": results}
    # # The output detectionary includes all the detected classes and their locations
    # num_detections = int(outputs.pop('num_detections'))
    # detection_classes = outputs['detection_classes'][0].numpy()[:num_detections]
    # detection_boxes = outputs['detection_boxes'][0].numpy()[:num_detections]
    
    
    # # Print results
    # print("Detected classes: ", detection_classes)
    # print("Detection boxes: ", detection_boxes)

    # for i in range(num_detections):
    #     box = detection_boxes[i]
    #     cv2.rectangle(image, (int(box[1]*image.shape[1]), int(box[0]*image.shape[0])),
    #                   (int(box[3]*image.shape[1]), int(box[2]*image.shape[0])),
    #                   (255, 0, 0), 2) # Blue colour for the box
        
        
    # # Display the image
    # cv2.imshow('Object detection', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    

    
    # Process outputs
    
    # return {"message" : "Image processed successfully"}

def process_image(image_path):
    # Implement image processing logic here
    # For example, use a pre-trained model to detect objects, classify objects, and segment the image
    # Return the detected objects, classifications, and segmentation results
    return {"status": "success", "data" : "Processed image details would be here"}


