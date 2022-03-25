import tensorflow as tf
from dataHandler import load_remote, CLASS_NUM, dataAugment
from model import getModel, get_regnet
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'
tf.random.set_seed(2345)

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


print('Loading data...')
_, test_imgs, test_labels, train_imgs, train_labels = load_remote(
    split_num=1, nor=True)
print('Data loaded.')
# print(train_imgs[0:1], train_labels.shape)

KERNEL_SIZE = 3
BATCH_SIZE = 256
EPOCH = 200


def train():
    gen = dataAugment(train_imgs, train_labels, batch_size=BATCH_SIZE)

    # reducing learning rate on plateau
    rlrop = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', mode='min', patience=5, factor=0.5, min_lr=1e-6, verbose=1)

    model = getModel(
        train_imgs.shape[1:], KERNEL_SIZE, CLASS_NUM, reg=True, normal=True)

    # model = get_regnet(train_imgs.shape[1:], CLASS_NUM)

    model.summary()

    # log_dir = "./logs/fit/"

    # tensorboard_callback = tf.keras.callbacks.TensorBoard(
    #     log_dir=log_dir, histogram_freq=1)

    # model.compile(
    #     optimizer='adam',
    #     loss='sparse_categorical_crossentropy',
    #     metrics=['accuracy'])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # callbacks=[tensorboard_callback]
    #   validation_data=(test_imgs, test_labels)
    h = model.fit(x=gen,  epochs=EPOCH, steps_per_epoch=50000 //
                  BATCH_SIZE, validation_data=(test_imgs, test_labels), callbacks=[rlrop])

    model.evaluate(test_imgs, test_labels)


train()
