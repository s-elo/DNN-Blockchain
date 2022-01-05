import os
from tensorflow.keras import layers, models
import tensorflow as tf
from utils import model_to_str

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


if __name__ == '__main__':
    from web3 import Web3
    print('web3 test here')

    model = getModel(input_shape=(32, 32, 3), kernel_size=3,
                     class_num=10, reg=True, normal=True)

    str_params, str_archi = model_to_str(model)

    print(len(str_params), len(str_archi))

    w3 = Web3(Web3.HTTPProvider(
        'https://ropsten.infura.io/v3/ab53629910c440089fda82f82af645f7'))

    print(w3.isConnected())
    balance = w3.eth.get_balance('0x8eacBB337647ea34eC26804C3339e80EB488587c')

    print(balance)
