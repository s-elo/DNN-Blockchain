import tensorflow as tf
from tensorflow.keras import layers, models


def getModel(input_shape, kernel_size, class_num, reg=False, normal=False):
    model = models.Sequential()

    # stage 1
    model.add(layers.Conv2D(filters=64, strides=1, kernel_size=kernel_size, activation='relu',
                            input_shape=input_shape, kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters=64, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # stage 2
    model.add(layers.Conv2D(filters=128, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters=128, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # stage 3
    model.add(layers.Conv2D(filters=256, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters=256, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())
        
    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # flatten as one dimension
    model.add(layers.Flatten())

    # fully connected layer 500 neurons
    model.add(layers.Dense(units=128, activation='relu',
              kernel_regularizer='l2' if reg else None))

    model.add(layers.Dropout(0.5))

    # final fully connected layer CLASS_NUM neurons with respect to CLASS_NUM subjects
    model.add(layers.Dense(units=class_num, activation='softmax',
              kernel_initializer='he_normal', kernel_regularizer='l2' if reg else None))

    return model
