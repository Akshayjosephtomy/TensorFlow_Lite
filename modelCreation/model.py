import tensorflow as tf
import pathlib
import PIL
import PIL.Image
import matplotlib.pyplot as plt
import numpy as np

# train_data_dir = pathlib.Path('dataset/train').with_suffix('')
# val_data_dir = pathlib.Path('dataset/validate').with_suffix('')
data_dir = pathlib.Path('animals').with_suffix('')

# image_count = len(list(data_dir.glob('*/*.jpg')))
# print(image_count)
# dogs = list(data_dir.glob('dog/*'))
# img = PIL.Image.open(str(dogs[2]))
# img.show()
# img = PIL.Image.open(str(dogs[5]))
# img.show()

batch_size = 32
img_height = 180
img_width = 180
input_shape = (img_height, img_width, 3)
learning_rate = 0.002
num_classes = 4

train_x = tf.keras.utils.get_file(

)

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

class_names = train_ds.class_names
print(class_names)

'''show 16 images of the set'''

# plt.figure(figsize=(10, 10))
# for images, labels in train_ds.take(1):
#     for i in range(16):
#         ax = plt.subplot(4, 4, i+1)
#         plt.imshow(images[i].numpy().astype('uint8'))
#         plt.title(class_names[labels[i]])
#         plt.axis('off')
# plt.show()

# normalization_layer = tf.keras.layers.Rescaling(1./255)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

'''train the model'''

data_augmentation = tf.keras.Sequential(
  [
    tf.keras.layers.RandomFlip("horizontal",
                               input_shape=input_shape
                               ),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
  ]
)


model = tf.keras.Sequential([
    data_augmentation,
    tf.keras.layers.Rescaling(1./255),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes)
])

model.compile(
  optimizer='adam',
  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=['accuracy']
)

# model.compile(optimizer=tf.keras.optimizers.SGD(lr=learning_rate, momentum=0.9),
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])


epochs = 20
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)

model.summary()
'''visualize the results of the training'''
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

model.save('saved/model3')





