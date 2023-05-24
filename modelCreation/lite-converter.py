import tensorflow as tf

saved_model_dir = 'saved/model3'
# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)  # path to the SavedModel directory
tflite_model = converter.convert()

with open('saved/lite/model3.tflite', 'wb') as f:
    f.write(tflite_model)
