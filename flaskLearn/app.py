from flask import Flask, request
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
img_height = 180
img_width = 180
class_names = ['cat', 'dog', 'monkey', 'squirrel']

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path='assets/models/model.tflite')
interpreter.allocate_tensors()


# @app.route('/')
# def hello_world():
#     return '<h1>Hello World!</h2>'


# @app.route("/name/<name>")
# def hello(name):
#     return f"Hello, {name}"


# @app.route("/Users", methods=['POST'])
# def set_users():
#     return f"Users are :\nArjun\nAmal\nAkshay"


@app.route("/result", methods=['POST'])
def get_result():
    src = request.get_json()
    # src_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRu24VGO83eZhYo6wozTsPVZlPvvO58_CcVcg&usqp=CAU'
    src_url = src['url']
    src_url_path = tf.keras.utils.get_file(origin=src_url)

    # Load and preprocess the image
    img = Image.open(src_url_path).resize((img_height, img_width))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
    # img.show()

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
    confidence = 100 - np.max(output_data)*10
    result = "This image most likely belongs to {} with a {:.2f} percent confidence.".format(predicted_class, confidence)
    return result
