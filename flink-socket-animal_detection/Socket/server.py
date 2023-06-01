import socket
import json
import tensorflow as tf
import numpy as np
from PIL import Image

img_height = 180
img_width = 180
class_names = ['cat', 'dog', 'monkey', 'squirrel']

# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path='assets/models/model3.tflite')
interpreter.allocate_tensors()

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 8888)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server started. Waiting for connections...")

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print("Client connected:", client_address)

    try:
        while True:
            # Receive the JSON data from the client
            data = client_socket.recv(1024).decode()
            print(data)
            if not data:
                break

            # Parse the received JSON string into a Python dictionary
            json_data = json.loads(data)

            # Extract the URL from the JSON data
            src_url = json_data['url']

            # Load and preprocess the image
            src_url_path = tf.keras.utils.get_file(origin=src_url)
            img = Image.open(src_url_path).resize((img_height, img_width))
            img_array = np.array(img)
            img_array = np.expand_dims(img_array, axis=0).astype(np.float32)

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
            confidence = 100 - np.max(output_data) * 10
            result = "This image most likely belongs to {} with a {:.2f} percent confidence.".format(predicted_class, confidence)

            # Encode the result as JSON
            json_result = json.dumps(result)

            # Send the JSON result to the client
            client_socket.sendall(json_result.encode())

    except Exception as e:
        print("An error occurred:", str(e))
        continue

    finally:
        # Close the client connection
        client_socket.close()
