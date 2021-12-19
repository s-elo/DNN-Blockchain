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


def split_train(dataset, test_imgs, test_labels):
    model = getModel(test_imgs.shape[1:], KERNEL_SIZE, CLASS_NUM)

    model.summary()

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    log_dir = "./logs/fit/"

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir, histogram_freq=1)

    gen = []
    for batchIdx in range(0, len(dataset)):
        train_imgs = dataset[batchIdx][0]
        train_labels = dataset[batchIdx][1]
        gen.append(dataAugment(train_imgs, train_labels, batch_size=BATCH_SIZE))

    for batchIdx in range(0, len(dataset)):
        print('\n')
        print('================Round' + str(batchIdx + 1) + '=================')

        train_imgs = dataset[batchIdx][0]
        train_labels = dataset[batchIdx][1]

        gen = dataAugment(train_imgs, train_labels, batch_size=BATCH_SIZE)

        model.fit(x=gen,  epochs=EPOCH, steps_per_epoch=train_imgs.shape[0] // BATCH_SIZE,
                  validation_data=(test_imgs, test_labels), callbacks=[tensorboard_callback])


split_train(dataset, test_imgs, test_labels)
