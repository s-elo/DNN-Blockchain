import tensorflow as tf
import numpy as np
import os
import cv2

root_path = '/media/HD2/chao/tiny_imagenet/tiny-imagenet-200'
train_path = f'{root_path}/train'
val_path = f'{root_path}/val'

height = 64
width = 64
channels = 3

class_num = 200

batch_size = 128
epochs = 40


def map_labels(path=f'{root_path}/wnids.txt'):
    label_map = {}

    # map the folder name as index order
    with open(path, 'r') as f:
        for idx, line in enumerate(f.readlines()):
            line = line.replace('\n', '')
            label_map[line] = idx

    return label_map


def load_train_list(train_path, label_map):
    images = []
    labels = []

    # get the image path and corresponding labels
    for label in os.listdir(path=train_path):
        for image_path in os.listdir(path=f'{train_path}/{label}/images'):
            images.append(f'{train_path}/{label}/images/{image_path}')
            labels.append(label_map[label])

    return images, labels


def load_test_list(val_path, label_map):
    images = []
    labels = []

    # get the image path and corresponding labels
    with open(f'{val_path}/val_annotations.txt', 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '').split('\t')
            images.append(f'{val_path}/images/{line[0]}')
            labels.append(label_map[line[1]])

    return images, labels


def preprocess(image_path, label):
    # get the real image data
    i = cv2.imread(image_path.numpy().decode())
    # resize
    i = cv2.resize(i, (height, width), interpolation=cv2.INTER_CUBIC)
    # normalization
    i = tf.cast(i, tf.float32)/255
    # convert the label into one hot format
    label = tf.one_hot(label, depth=class_num)

    return (i, label)


def get_dataset():
    label_map = map_labels()
    train_x, train_y = load_train_list(train_path, label_map)
    test_x, test_y = load_test_list(val_path, label_map)

    train_set = tf.data.Dataset.from_tensor_slices((train_x, train_y))
    test_set = tf.data.Dataset.from_tensor_slices((test_x, test_y))

    train_set = train_set.map(lambda x, y: tf.py_function(preprocess, inp=[x, y], Tout=[tf.float32, tf.float32]),
                              num_parallel_calls=tf.data.experimental.AUTOTUNE)
    train_set = train_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    train_set = train_set.shuffle(len(train_set)).cache().batch(batch_size)

    test_set = test_set.map(lambda x, y: tf.py_function(preprocess, inp=[x, y], Tout=[tf.float32, tf.float32]),
                            num_parallel_calls=tf.data.experimental.AUTOTUNE)
    test_set = test_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    test_set = test_set.shuffle(len(test_set)).cache().batch(batch_size)

    print(len(train_set), len(test_set))
    return train_set, test_set


if __name__ == '__main__':
    # label_map = map_labels()
    # print(label_map)

    # train_x, train_y = load_train_list(train_path, label_map)
    # test_x, test_y = load_test_list(val_path, label_map)

    # print(train_x[0:2], train_y[0:2], test_x[0:2], test_y[0:2])
    get_dataset()
