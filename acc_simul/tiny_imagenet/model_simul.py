import tensorflow as tf
from dataHandler import get_dataset, load_numpy_data, dataAugment, batch_size, epochs, class_num, height, width, channels, steps_per_epoch
from model import getModel
import os
import random
import numpy as np

seed = 42

random.seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)
np.random.seed(seed)
tf.keras.utils.set_random_seed(seed)

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


print('Loading data...')
# train_set, test_set = get_dataset()
x_train, y_train, x_test, y_test = load_numpy_data()
print('Data loaded.')


def train():
    gen = dataAugment(x_train, y_train, batch_size=batch_size)

    model = getModel((height, width, channels), kernel_size=3,
                     class_num=class_num, reg=True, normal=True)

    # model = get_regnet(train_imgs.shape[1:], CLASS_NUM)

    model.summary()

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # model.fit(train_set, epochs=epochs, validation_data=test_set)
    model.fit(gen, epochs=epochs, batch_size=batch_size,
              steps_per_epoch=steps_per_epoch, validation_data=(x_test, y_test))


train()
