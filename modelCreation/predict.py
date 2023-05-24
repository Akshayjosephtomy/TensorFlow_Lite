import tensorflow as tf
import numpy as np
from tensorflow import keras

img_height = 180
img_width = 180
class_names = ['cat', 'dog', 'monkey', 'squirrel']

model = keras.models.load_model('saved/model1')
src_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/The_Indian_Pariah_Dog.jpg/1200px-The_Indian_Pariah_Dog.jpg'
src_url_path = keras.utils.get_file(origin=src_url)

img = keras.utils.load_img(
    src_url_path, target_size=(img_height, img_width)
)
img_array = keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)
img.show()
# Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
