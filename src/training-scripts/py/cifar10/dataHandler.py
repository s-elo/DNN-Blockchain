import os
import numpy as np
from random import shuffle
from PIL import Image
from tensorflow.keras.utils import to_categorical

TRAIN_PATH = './dataset/train'
TEST_PATH = './dataset/test'

CLASS_NAMES = os.listdir(TRAIN_PATH)
CLASS_NUM = len(CLASS_NAMES)

IMG_WIDTH = 32
IMG_HEIGHT = 32
IMG_CHANNEL = 3


def load_data(type='TRAIN'):
    imgs = []
    labels = []

    if (type == 'TRAIN'):
        data_path = TRAIN_PATH
    elif (type == 'TEST'):
        data_path = TEST_PATH

    for classIdx in range(0, len(CLASS_NAMES)):
        imgNames = os.listdir(data_path + '/' + CLASS_NAMES[classIdx])

        for idx in range(0, len(imgNames)):
            # get one image
            img = Image.open(data_path + '/' +
                             CLASS_NAMES[classIdx] + '/' + imgNames[idx]).resize((IMG_WIDTH, IMG_HEIGHT))

            # convert into a vector
            img_vector = np.array(img).reshape(
                IMG_WIDTH*IMG_HEIGHT*IMG_CHANNEL)/255

            imgs.append(img_vector)
            labels.append(classIdx)
            
    x = np.array(imgs).reshape(len(imgs), IMG_WIDTH, IMG_HEIGHT, IMG_CHANNEL)
    y = to_categorical(labels, num_classes=CLASS_NUM)

    # return (np.array(imgs).reshape(len(imgs), IMG_WIDTH, IMG_HEIGHT, IMG_CHANNEL), np.array(labels))
    return shuffle_dataset(x, y)


def shuffle_dataset(x, y):
    ind_list = [i for i in range(y.shape[0])]
    shuffle(ind_list)
    x_new = x[ind_list, :, :, :]
    y_new = y[ind_list, ]

    return (x_new, y_new)
