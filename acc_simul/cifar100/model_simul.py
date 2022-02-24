import tensorflow as tf
from dataHandler import load_data, CLASS_NUM, dataAugment
from model import getModel
import numpy as np
from modelStorage import str_to_model, model_to_str

print('Loading data...')
train_imgs, train_labels = load_data(type='TRAIN')
test_imgs, test_labels = load_data(type='TEST')

print('Data loaded.')
# print(train_imgs[0:1], train_labels.shape)

KERNEL_SIZE = 3
BATCH_SIZE = 256
EPOCH = 5


def train():
    gen = dataAugment(train_imgs, train_labels, batch_size=BATCH_SIZE)

    model = getModel(train_imgs.shape[1:], KERNEL_SIZE, CLASS_NUM, reg=True, normal=True)

    model.summary()

    log_dir = "./logs/fit/"

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir, histogram_freq=1)

    # def scheduler(epoch, lr):
    #     if (epoch == 1):
    #         return 0.01
    #     if epoch % 10 == 0:
    #         return lr - 0.0005
    #     else:
    #         return lr

    # learn_scheduler_callback = tf.keras.callbacks.LearningRateScheduler(
    #     scheduler)

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    h = model.fit(x=gen,  epochs=EPOCH, steps_per_epoch=50000 // BATCH_SIZE,
                  callbacks=[tensorboard_callback])

    model.evaluate(test_imgs, test_labels)

    str_weights, str_model_structure = model_to_str(model)

    print(type(str_weights), type(str_model_structure))
    new_model = str_to_model(str_weights, str_model_structure)

    new_model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    model.evaluate(test_imgs, test_labels)
    # model.fit(train_imgs, train_labels, epochs=EPOCH, batch_size=BATCH_SIZE, shuffle=True,
    #           validation_data=(test_imgs, test_labels),
    #           callbacks=[tensorboard_callback])

    # model.save('CIFAR10_model_with_data_augmentation_dual_GPU.h5')
    # validation_data=(test_imgs, test_labels),

train()
