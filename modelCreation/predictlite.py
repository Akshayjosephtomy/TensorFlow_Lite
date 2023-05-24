import tensorflow as tf
import numpy as np
from PIL import Image

img_height = 180
img_width = 180
class_names = ['cat', 'dog', 'monkey', 'squirrel']

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path='saved/lite/model.tflite')
interpreter.allocate_tensors()

src_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRu24VGO83eZhYo6wozTsPVZlPvvO58_CcVcg&usqp=CAU'
src_url_path = tf.keras.utils.get_file(origin=src_url)

# Load and preprocess the image
img = Image.open(src_url_path).resize((img_height, img_width))
img_array = np.array(img)
img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
img.show()

# Set the input tensor to the TensorFlow Lite model
input_details = interpreter.get_input_details()
interpreter.set_tensor(input_details[0]['index'], img_array)

# Run the inference
interpreter.invoke()

# Get the output tensor from the TensorFlow Lite model
output_details = interpreter.get_output_details()
output_data = interpreter.get_tensor(output_details[0]['index'])

# Get the predicted class label
predicted_index = np.argmax(output_data)
predicted_class = class_names[predicted_index]
confidence = np.max(output_data)

result = "This image most likely belongs to {} with a {:.2f} percent confidence.".format(predicted_class, confidence)
print(result)
