import os
import numpy as np
from random import shuffle
from PIL import Image
from tensorflow.keras.utils import to_categorical
import json
import requests as rq


def get_testset(modelName):
    print('loading the testset...')
    if modelName == 'cifar10':
        testset = rq.get(
            f'http://localhost:8080/ipfs/QmXqes1bAQzDjyTD3pNTV6fK5a8LEqy8HiDCS5nJ4FbD9z').json()

        return (np.array(testset['data']), np.array(testset['label']))
        # return get_cifar10()


def get_cifar10():
    imgs = []
    labels = []

    if __name__ == '__main__':
        data_path = f'{os.getcwd()}/cifar10'
    else:
        data_path = f'{os.getcwd()}/testset/cifar10'

    CLASS_NAMES = os.listdir(data_path)
    IMG_WIDTH = 32
    IMG_HEIGHT = 32
    IMG_CHANNEL = 3

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
    y = to_categorical(labels, num_classes=len(CLASS_NAMES))

    # return (np.array(imgs).reshape(len(imgs), IMG_WIDTH, IMG_HEIGHT, IMG_CHANNEL), np.array(labels))
    return shuffle_dataset(x, y)


def shuffle_dataset(x, y):
    ind_list = [i for i in range(y.shape[0])]
    shuffle(ind_list)
    x_new = x[ind_list, :, :, :]
    y_new = y[ind_list, ]

    return (x_new, y_new)


if __name__ == '__main__':
    import ipfshttpclient as ipfs

    client = ipfs.connect()

    # test_data, test_label = get_testset('cifar10')
    # print(test_data.shape, test_label.shape)

    # testset_hash = client.add_json({
    #     'data': test_data.tolist(),
    #     'label': test_label.tolist()
    # })

    # print(testset_hash)

    testset = rq.get(
        f'http://localhost:8080/ipfs/QmXqes1bAQzDjyTD3pNTV6fK5a8LEqy8HiDCS5nJ4FbD9z').json()

    test_data = testset['data']
    print(np.array(test_data).shape)
