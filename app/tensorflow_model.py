import tensorflow as tf

# Load the pre-trained model
model = tf.saved_model.load('/app/data/modelset/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar')

# Prepare the model for inference
infer = model.signatures['serving_default']

