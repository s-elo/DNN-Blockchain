import os
import numpy as np
from random import shuffle
from PIL import Image
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

TRAIN_PATH = './dataset/'

CLASS_NAMES = os.listdir(TRAIN_PATH)
CLASS_NUM = len(CLASS_NAMES)

IMG_WIDTH = 32
IMG_HEIGHT = 32
IMG_CHANNEL = 3


def load_split_train_data():
    data_path = TRAIN_PATH
    dataset = []

    # initialize the dataset array
    for _ in range(0, 5):
        imgs = []
        labels = []
        dataset.append((imgs, labels))

    # start to split
    for classIdx in range(0, CLASS_NUM):
        imgNames = os.listdir(data_path + '/' + CLASS_NAMES[classIdx])

        imgIdx = 0
        # 0-4
        batchIdx = 0
        while (imgIdx < len(imgNames)):
            # every 1000 imgs in the current class are stored in a new batch
            if (imgIdx % 1000 == 0 and imgIdx != 0):
                batchIdx += 1

            # get one image
            img = Image.open(data_path + '/' +
                             CLASS_NAMES[classIdx] + '/' + imgNames[imgIdx]).resize((IMG_WIDTH, IMG_HEIGHT))

            # convert into a vector
            img_vector = np.array(img).reshape(
                IMG_WIDTH*IMG_HEIGHT*IMG_CHANNEL)/255

            # add to the current batch
            dataset[batchIdx][0].append(img_vector)
            dataset[batchIdx][1].append(classIdx)

            imgIdx += 1

    # reconstruct the batches
    for batchIdx in range(0, 5):
        cur_batch_imgs = dataset[batchIdx][0]
        cur_batch_labels = dataset[batchIdx][1]

        x = np.array(cur_batch_imgs).reshape(
            len(cur_batch_imgs), IMG_WIDTH, IMG_HEIGHT, IMG_CHANNEL)
        y = to_categorical(
            cur_batch_labels, num_classes=CLASS_NUM)

        dataset[batchIdx] = shuffle_dataset(x, y)

    return dataset


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
    dataset = load_split_train_data()
    print(len(dataset), dataset[0][0].shape)
