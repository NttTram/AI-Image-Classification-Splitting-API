import cv2 
import numpy as np
import tensorflow as tf



# Load the pre-trained model
model = tf.saved_model.load('/app/data/modelset/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar')

# Prepare the model for inference
infer = model.signatures['serving_default']

#----------------------------------------------------------------
# Load image
image = cv2.imread('/app/data/images/fruits.jpg')

# Convert image to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Resize and expand dimensions to fit the model input
image_resize = cv2.resize(image_rgb, (320,320))
input_tensor = tf.convert_to_tensor([image_resize], dytype=tf.float32)

#----------------------------------------------------------------
# Run detection
output_dict = infer(input_tensor)

# The output directionary includes all the detected classes and their locations
num_detections = int(output_dict.pop('num_detections'))
detection_classes = output_dict['detection_classes'][0].numpy()[:num_detections]
detection_boxes = output_dict['detection_boxes'][0].numpy()[:num_detections]

# Print results
print("Detected classes: ", detection_classes)
print("Detection boxes: ", detection_boxes)
    

for i in range(num_detections):
    box = detection_boxes[i]
    cv2.rectangle(image, (int(box[1]*image.shape[1]), int(box[0]*image.shape[0])), 
                  (int(box[3]*image.shape[1]), int(box[2]*image.shape[0])), 
                  (255, 0, 0), 2)  # Blue color for the box

# Display the image
cv2.imshow('Object detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
