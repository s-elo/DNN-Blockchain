import collections
import numpy as np
import tensorflow as tf
from dataHandler import load_split_train_data, load_data, dataAugment, CLASS_NUM
from model import getModel

print('Loading data...')
dataset = load_split_train_data()
test_imgs, test_labels = load_data(type='TEST')
print('Data loaded.')
print(len(dataset), dataset[0][0].shape, dataset[0][1].shape)

KERNEL_SIZE = 3
BATCH_SIZE = 64
EPOCH = 20

model = getModel(test_imgs.shape[1:], KERNEL_SIZE, CLASS_NUM)

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()


def split_train(model, dataset, test_imgs, test_labels):
    weights = model.get_weights()

    log_dir = "./logs/fit/"

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir, histogram_freq=1)

    new_weights = []
    for batchIdx in range(0, len(dataset)):
        print('\n')
        print('================User' + str(batchIdx + 1) + '=================')

        train_imgs = dataset[batchIdx][0]
        train_labels = dataset[batchIdx][1]

        gen = dataAugment(train_imgs, train_labels, batch_size=BATCH_SIZE)

        model.set_weights(weights)

        model.fit(x=gen,  epochs=EPOCH, steps_per_epoch=train_imgs.shape[0] // BATCH_SIZE,
                  validation_data=(test_imgs, test_labels), callbacks=[tensorboard_callback])

        new_weights.append(model.get_weights())

    return new_weights


def fedAvg(model, new_weights=[]):
    sum_weights = 0

    for i in range(0, len(new_weights)):
        sum_weights += np.array(new_weights[i], dtype=object)

    mean_weights = sum_weights / len(new_weights)

    model.set_weights(mean_weights.tolist())
    return model


ROUND = 6


def fl():
    avg_model = model
    for i in range(0, ROUND):
        print('\n')
        print('================Round' + str(i + 1) + '=================')

        new_weights = split_train(avg_model, dataset, test_imgs, test_labels)
        avg_model = fedAvg(model, new_weights)

        avg_model.evaluate(test_imgs, test_labels)


fl()
