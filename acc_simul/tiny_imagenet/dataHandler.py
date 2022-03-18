import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
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

batch_size = 256
epochs = 200

steps_per_epoch = 100000 // batch_size

img_augmentation = tf.keras.models.Sequential(
    [
        layers.RandomRotation(factor=0.15),
        layers.RandomTranslation(height_factor=0.1, width_factor=0.1),
        layers.RandomFlip(),
        layers.RandomContrast(factor=0.1),
    ],
    name="img_augmentation",
)


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


def preprocess_wrap(image_path, label):
    image, label = tf.py_function(preprocess, inp=[image_path, label], Tout=[
                                  tf.float32, tf.float32])
    image.set_shape((height, width, channels))
    label.set_shape((class_num,))

    return image, label


def preprocess(image_path, label):
    # get the real image data
    i = cv2.imread(image_path.numpy().decode())
    # resize
    i = cv2.resize(i, (height, width), interpolation=cv2.INTER_CUBIC)
    # normalization
    i = tf.cast(i, tf.float32)/255
    # data augmentation
    i = img_augmentation(i, training=True)
    # convert the label into one hot format
    label = tf.one_hot(label, depth=class_num)

    return (i, label)


def get_dataset():
    label_map = map_labels()
    train_x, train_y = load_train_list(train_path, label_map)
    test_x, test_y = load_test_list(val_path, label_map)

    train_set = tf.data.Dataset.from_tensor_slices((train_x, train_y))
    test_set = tf.data.Dataset.from_tensor_slices((test_x, test_y))

    train_set = train_set.map(preprocess_wrap)
    train_set = train_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    train_set = train_set.shuffle(len(train_set)).cache().batch(batch_size)

    test_set = test_set.map(preprocess_wrap)
    test_set = test_set.prefetch(buffer_size=tf.data.AUTOTUNE)
    test_set = test_set.shuffle(len(test_set)).cache().batch(batch_size)

    return train_set, test_set


def load_numpy_data():
    label_map = map_labels()

    # load training set
    train_images = []
    train_labels = []

    # get the image path and corresponding labels
    for label in os.listdir(path=train_path):
        for image_path in os.listdir(path=f'{train_path}/{label}/images'):
            # get the real image data
            i = cv2.imread(f'{train_path}/{label}/images/{image_path}')
            # resize
            i = cv2.resize(i, (height, width), interpolation=cv2.INTER_CUBIC)
            # reshape
            i = np.reshape(i, (height, width, channels)) / 255

            train_images.append(i)

            train_labels.append(label_map[label])

    # convert into one hot format
    train_labels = tf.keras.utils.to_categorical(
        np.array(train_labels).reshape((len(train_labels), 1)), num_classes=class_num)

    # load test set
    test_images = []
    test_labels = []

    # get the image path and corresponding labels
    with open(f'{val_path}/val_annotations.txt', 'r') as f:
        for line in f.readlines():
            line = line.replace('\n', '').split('\t')

            # get the real image data
            i = cv2.imread(f'{val_path}/images/{line[0]}')
            # resize
            i = cv2.resize(i, (height, width), interpolation=cv2.INTER_CUBIC)
            # reshape
            i = np.reshape(i, (height, width, channels)) / 255

            test_images.append(i)
            test_labels.append(label_map[line[1]])

    # convert into one hot format
    test_labels = tf.keras.utils.to_categorical(
        np.array(test_labels).reshape((len(test_labels), 1)), num_classes=class_num)

    return (np.array(train_images), train_labels, np.array(test_images), test_labels)


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


if __name__ == '__main__':
    # label_map = map_labels()
    # print(label_map)

    # train_x, train_y = load_train_list(train_path, label_map)
    # test_x, test_y = load_test_list(val_path, label_map)

    # print(train_x[0:2], train_y[0:2], test_x[0:2], test_y[0:2])
    # train_set, test_set = get_dataset()
    # print(len(train_set), len(test_set))

    x_train, y_train, x_test, y_test = load_numpy_data()
    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)
