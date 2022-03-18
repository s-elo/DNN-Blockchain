from tensorflow.keras import layers, models
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.efficientnet import EfficientNetB0
from tensorflow.keras.models import Sequential
import os
import random
import numpy as np
import tensorflow as tf

seed = 42

random.seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)
np.random.seed(seed)
tf.keras.utils.set_random_seed(seed)


def getModel(input_shape, kernel_size, class_num, reg=True, normal=True):
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

    # stage 4
    model.add(layers.Conv2D(filters=512, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(filters=512, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # stage 5
    model.add(layers.Conv2D(filters=512, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(filters=512, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # flatten as one dimension
    model.add(layers.Flatten())

    # fully connected layer 256 neurons
    model.add(layers.Dense(units=256, activation='relu',
              kernel_regularizer='l2' if reg else None))
    model.add(layers.Dropout(0.5))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.Dense(units=128, activation='relu',
              kernel_regularizer='l2' if reg else None))

    # final fully connected layer CLASS_NUM neurons with respect to CLASS_NUM subjects
    model.add(layers.Dense(units=class_num, activation='softmax',
              kernel_initializer='he_normal', kernel_regularizer='l2' if reg else None))

    return model


def get_pretrained_model(input_shape, class_num):
    res_model = ResNet50(include_top=False, weights='imagenet',
                         classes=class_num, input_shape=input_shape)
    res_model.trainable = True

    # print("Number of layers in the base model: ", len(res_model.layers))

    # # Fine-tune from this layer onwards
    # fine_tune_at = 20

    # # Freeze all the layers before the `fine_tune_at` layer
    # for layer in res_model.layers[:fine_tune_at]:
    #     layer.trainable = False

    # inputs = tf.keras.Input(shape=input_shape)
    # x = res_model(inputs)
    # x = tf.keras.layers.GlobalAveragePooling2D()(x)
    # x = tf.keras.layers.Dropout(0.2)(x)
    # outputs = tf.keras.layers.Dense(class_num, activation='softmax')(x)
    # model = tf.keras.Model(inputs, outputs)

    model = Sequential()
    model.add(res_model)
    model.add(tf.keras.layers.GlobalAveragePooling2D())
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(class_num, activation='softmax'))
    model.summary()

    return model
