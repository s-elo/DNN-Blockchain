import numpy as np
import random
import os
from model import getModel, get_pretrained_model
from dataHandler import load_numpy_data, dataAugment, batch_size, epochs, class_num, height, width, channels, steps_per_epoch
import tensorflow as tf

seed = 42

random.seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)
np.random.seed(seed)
tf.keras.utils.set_random_seed(seed)


print('Loading data...')
# train_set, test_set = get_dataset()
x_train, y_train, x_test, y_test = load_numpy_data()
print('Data loaded.')


def train():
    gen = dataAugment(x_train, y_train, batch_size=batch_size)

    # reducing learning rate on plateau
    rlrop = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', mode='min', patience=5, factor=0.5, min_lr=1e-6, verbose=1)

    # model = getModel((height, width, channels), kernel_size=3,
    #                  class_num=class_num, reg=True, normal=True)

    model = get_pretrained_model((height, width, channels), class_num)

    model.summary()

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # model.fit(train_set, epochs=epochs, validation_data=test_set)
    model.fit(gen, epochs=epochs, batch_size=batch_size,
              steps_per_epoch=steps_per_epoch, validation_data=(x_test, y_test), callbacks=[rlrop])


train()
