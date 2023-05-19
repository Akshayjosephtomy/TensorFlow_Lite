import tensorflow as tf
import numpy as np
from tensorflow import keras
from PIL import Image

img_height = 180
img_width = 180
class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

model = keras.models.load_model('flower_model')

src_url = 'https://www.flower.style/assets/images/NoCrop_536/4b4dd419eca9451db2f79a190c10edca.jpg'
src_url_path = keras.utils.get_file('tulips', origin=src_url)

img = keras.utils.load_img(
    src_url_path, target_size=(img_height, img_width)
)

img_array = keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

img.show()

# Create a batch
predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

# Align and display the result
prediction_text = "This image most likely belongs to {:<10} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score))
print(prediction_text)
