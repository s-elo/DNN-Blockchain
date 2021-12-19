from test_model import getModel
from modelStorage import model_to_str, str_to_model
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import numpy as np
import json

EPOCH = 1
nb_classes = 10
# Load CIFAR-10 dataset
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()

y_train = y_train.reshape(y_train.shape[0])
y_test = y_test.reshape(y_test.shape[0])
y_train = to_categorical(y_train, nb_classes)
y_test = to_categorical(y_test, nb_classes)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

model = getModel((32, 32, 3), 5, 10)
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=EPOCH)
model.evaluate(X_test, y_test)

str_weights, str_model_structure = model_to_str(model)

model_new = str_to_model(str_weights, str_model_structure)

print(model.metrics_names)

model_new.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
model_new.evaluate(X_test, y_test)

print(model.metrics_names)
