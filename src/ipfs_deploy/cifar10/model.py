import os
from tensorflow.keras import layers, models
import tensorflow as tf
import sys
sys.path.append('..')
from utils import model_to_str, save

os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


def get_model(input_shape, kernel_size, class_num, reg=True, normal=True):
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


def get_cifar10_model():
    model = get_model(input_shape=(32, 32, 3), kernel_size=3,
                      class_num=10, reg=True, normal=True)

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    str_params, str_archi = model_to_str(model)

    data = {'params': str_params, 'archi': str_archi}

    return data


def create_file():
    data = get_cifar10_model()

    save('./model.json', data)

create_file()
