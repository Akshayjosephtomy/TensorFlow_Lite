import tensorflow as tf
import numpy as np
from tensorflow import keras
from PIL import Image

img_height = 180
img_width = 180
class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path='flower_model.tflite')
interpreter.allocate_tensors()

src_url = 'https://m.media-amazon.com/images/I/61sX88rhCoL._SX425_.jpg'
src_url_path = keras.utils.get_file('sunflower1', origin=src_url)

img = keras.utils.load_img(
    src_url_path, target_size=(img_height, img_width)
)

img_array = keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

img.show()

# Set input tensor to the TFLite model
input_details = interpreter.get_input_details()
interpreter.set_tensor(input_details[0]['index'], img_array)

# Run inference
interpreter.invoke()

# Get the output tensor from the TFLite model
output_details = interpreter.get_output_details()
output_data = interpreter.get_tensor(output_details[0]['index'])

# Convert the output tensor to probabilities
scores = tf.nn.softmax(output_data[0])

# Get the predicted label and confidence
predicted_index = np.argmax(scores)
confidence = 100 * scores[predicted_index]

# Get the predicted class name
predicted_class = class_names[predicted_index]

# Display the result
prediction_text = "This image most likely belongs to {:<10} with a {:.2f} percent confidence.".format(predicted_class, confidence)
print(prediction_text)
