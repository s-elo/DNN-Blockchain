import numpy as np
from random import shuffle
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

CLASS_NUM = 100


def load_remote(split_num=1, nor=True):
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar100.load_data()

    # do the shuffle
    x_train, y_train = shuffle_dataset(x_train, y_train)

    if nor == True:
        x_train = x_train / 255
        x_test = x_test / 255

    y_train = to_categorical(y_train, num_classes=CLASS_NUM)
    y_test = to_categorical(y_test, num_classes=CLASS_NUM)

    # split the training data
    train_split_data = list(
        zip(np.split(x_train, split_num, axis=0), np.split(y_train, split_num, axis=0)))

    return (train_split_data, x_test, y_test, x_train, y_train)


def dataAugment(x, y, batch_size=256):
    aug_gen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        # randomly rotate images in the range (degrees, 0 to 180)
        rotation_range=0,
        # randomly shift images horizontally (fraction of total width)
        width_shift_range=0.1,
        # randomly shift images vertically (fraction of total height)
        height_shift_range=0.1,
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False,  # randomly flip images
    )

    aug_gen.fit(x)
    gen = aug_gen.flow(x, y, batch_size=batch_size)

    return gen


def shuffle_dataset(x, y):
    ind_list = [i for i in range(y.shape[0])]
    shuffle(ind_list)
    x_new = x[ind_list, :, :, :]
    y_new = y[ind_list, ]

    return (x_new, y_new)


if __name__ == '__main__':
    arr1 = np.array([[1, 2], [2, 3], [4, 5], [6, 7]])
    arr2 = np.array([[1], [2], [3], [4]])
    # x_shuffle, y_shuffle = shuffle_dataset(arr1, arr2)
    # print(x_shuffle, y_shuffle)
    print(np.split(arr1, 1, axis=0), np.split(arr2, 1, axis=0))
    print(list(zip(arr1, arr2)))
    load_remote()
