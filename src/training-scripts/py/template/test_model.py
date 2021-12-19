import tensorflow as tf
from tensorflow.keras import layers, models


def getModel(input_shape, kernel_size, class_num):
    model = models.Sequential()

    # stage 1
    model.add(layers.Conv2D(filters=64, strides=1, kernel_size=kernel_size, activation='relu',
                            input_shape=input_shape, kernel_initializer='he_normal', padding='same'))

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # flatten as one dimension
    model.add(layers.Flatten())

    # final fully connected layer CLASS_NUM neurons with respect to CLASS_NUM subjects
    model.add(layers.Dense(units=class_num, activation='softmax',
              kernel_initializer='he_normal'))

    return model
