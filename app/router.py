from fastapi import APIRouter, UploadFile, File, Response
import uuid
from fastapi.responses import JSONResponse
import os
import tensorflow as tf
import numpy as np
import cv2
import tempfile
import shutil
router = APIRouter()


# Load the pre-trained model
model_dir = '/app/data/modelset/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model'
print("Loading model from:", model_dir)
print("Is path correct?", os.path.exists(model_dir))

model = tf.saved_model.load(model_dir)

# Temporary directory to store detected imgs
# Ensure base image directory exists
img_dir = '/app/data/img/'
# Ensure the base directory exists
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
    print(f"Created base image directory at: {img_dir}")
else:
    print(f"Base image directory already exists at: {img_dir}")


    

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


def non_max_suppression(boxes, scores, threshold=0.35):
    if len(boxes) == 0:
        return []
    boxes = np.array(boxes)
    scores = np.array(scores)
    indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), score_threshold=0.3, nms_threshold=threshold)
    return indices.flatten()


# def draw_detections(image, boxes, classes, scores, class_names, threshold=0.35):
#     for i, score in enumerate(scores):
#         if score >= threshold:  # Ensure we are only drawing detections that meet the confidence threshold
#             x_min, y_min, x_max, y_max = boxes[i]
#             class_id = classes[i]
#             label = class_names.get(class_id, f'Unlabeled (ID {class_id})')
#             cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
#             cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#     return image



@router.post("/detect/")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Prepare the image for the model
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_img = cv2.resize(img, (320, 320))
    input_tensor = tf.convert_to_tensor([resized_img], dtype=tf.uint8)
    
    
    # print(model.signatures['serving_default'].inputs)
    # print("Shape of input tensor:", input_tensor.shape)
    # print("Data type of input tensor:", input_tensor.dtype)

    # Inference
    infer = model.signatures['serving_default']
    
    # Run detections
    outputs = infer(input_tensor)
   
    
    # Extracting outputs
    detection_boxes = outputs['detection_boxes'].numpy()[0]   # [1, num_detections, 4]
    detection_classes = outputs['detection_classes'].numpy()[0].astype(int)  # [1, num_detections]
    detection_scores = outputs['detection_scores'].numpy()[0]  # [1, num_detections]
    
    
    # Convert detection boxes from relative coordinates to absolute coordinates
    boxes = []
    for box in detection_boxes:
        ymin, xmin, ymax, xmax = box
        x_min, x_max = int(xmin * image.shape[1] - 40), int(xmax * image.shape[1] + 40)
        y_min, y_max = int(ymin * image.shape[0] - 40), int(ymax * image.shape[0] + 40)
        boxes.append([x_min, y_min, x_max, y_max])
    
    
    
    
    # Apply non-max suppression
    indices = non_max_suppression(boxes, detection_scores)
    
    
    # Keep track of class name to handle duplicates
    class_count = {}
    
    for i in indices:
        class_id = detection_classes[i]
        class_name = class_names.get(class_id, f"Unlabeled_{class_id}")
        
        # Increment count to handle duplicates
        class_count[class_name] = class_count.get(class_name, 0) + 1
        
        filename = f"{class_name}_{class_count[class_name]}.jpg"
        file_path = os.path.join(img_dir, filename)
        
        
        # # Crop, resize, and save each detected object
        # x_min, y_min, x_max, y_max = boxes[i]
        # cropped_image = image[y_min:y_max, x_min:x_max]
        # resized_cropped_image = cv2.resize(cropped_image, (360, 360))
        # _, encoded_image = cv2.imencode('.jpg', resized_cropped_image)
        # with open(file_path, 'wb') as file:
        #     file.write(encoded_image)
        try:
            # Crop and save each detected object
            x_min, y_min, x_max, y_max = (int(detection_boxes[i][1] * image.shape[1]),
                                            int(detection_boxes[i][0] * image.shape[0]),
                                            int(detection_boxes[i][3] * image.shape[1]),
                                            int(detection_boxes[i][2] * image.shape[0]))
            cropped_image = image[y_min:y_max, x_min:x_max]
            resized_cropped_image = cv2.resize(cropped_image, (360, 360))
            success = cv2.imwrite(file_path, resized_cropped_image)
            print("Image save successful: ", success)
            
            if not success:
                raise Exception("Could not write image to file system.")
            
        except Exception as e:
            print(f"Error saving image {filename}: {str(e)}")
        
    # filtered_boxes = [boxes[i] for i in indices]
    # filtered_classes = [detection_classes[i] for i in indices]
    # filtered_scores = [detection_scores[i] for i in indices]
    
    # # Draw detections
    # processed_image = draw_detections(image, filtered_boxes, filtered_classes, filtered_scores, class_names)
    
    
    # # Convert the image to JPEG format before sending the response
    # _, encoded_image = cv2.imencode('.jpg', processed_image)

    # return Response(content=encoded_image.tobytes(), media_type='image/jpeg')
    return {"message": "Image detection completed", "files_saved_to: ": img_dir}


# def clean_temp_dir():
#     shutil.rmtree(temp_dir)
#     print("Temporary files deleted")