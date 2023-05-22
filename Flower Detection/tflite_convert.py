import tensorflow as tf

# Convert the model to TensorFlow Lite format with optimization
converter = tf.lite.TFLiteConverter.from_saved_model('flower_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Save the optimized TensorFlow Lite model
with open('flower_model.tflite', 'wb') as f:
    f.write(tflite_model)
