import os
from dataHandler import dataAugment
import tensorflow as tf
from config import EPOCH, BATCH_SIZE

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

def train(model, train_data):
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    train_imgs = train_data[0]
    train_labels = train_data[1]

    gen = dataAugment(train_imgs, train_labels, batch_size=BATCH_SIZE)

    model.fit(x=gen,  epochs=EPOCH,
              steps_per_epoch=train_imgs.shape[0] // BATCH_SIZE)

    return model


def evaluate(model, test_data):
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    test_imgs = test_data[0]
    test_labels = test_data[1]

    model.evaluate(test_imgs, test_labels)
