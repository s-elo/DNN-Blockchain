import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from dataHandler import load_split_train_data, load_data, dataAugment, CLASS_NUM, load_remote
from model import getModel
import shutil
import os

if os.path.exists('./ret_img') == True:
    shutil.rmtree('./ret_img')
os.mkdir('./ret_img')

KERNEL_SIZE = 3
BATCH_SIZE = 256
EPOCH = 20
ROUND = 10
USER_NUM = 5

print('Loading data...')
dataset, test_imgs, test_labels, _, _ = load_remote(USER_NUM)
# dataset = load_split_train_data()
# test_imgs, test_labels = load_data(type='TEST')
print('Data loaded.')
print(len(dataset), dataset[0][0].shape, dataset[0][1].shape)

users_acc = [[]]*USER_NUM
users_val_acc = [[]]*USER_NUM
users_loss = [[]]*USER_NUM
users_val_loss = [[]]*USER_NUM

overall_val_acc = []*ROUND
overall_val_loss = []*ROUND

model = getModel(test_imgs.shape[1:], KERNEL_SIZE, CLASS_NUM)

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()


def split_train(model, dataset, test_imgs, test_labels):
    weights = model.get_weights()

    new_weights = []
    for batchIdx in range(0, len(dataset)):
        print('\n')
        print('================User' + str(batchIdx + 1) + '=================')

        train_imgs = dataset[batchIdx][0]
        train_labels = dataset[batchIdx][1]

        gen = dataAugment(train_imgs, train_labels, batch_size=BATCH_SIZE)

        model.set_weights(weights)

        h = model.fit(x=gen,  epochs=EPOCH, steps_per_epoch=train_imgs.shape[0] // BATCH_SIZE,
                      validation_data=(test_imgs, test_labels))

        acc = h.history['accuracy']
        loss = h.history['loss']
        val_acc = h.history['val_accuracy']
        val_loss = h.history['val_loss']

        users_acc[batchIdx] = users_acc[batchIdx] + acc

        users_val_acc[batchIdx] = users_val_acc[batchIdx] + val_acc
        users_loss[batchIdx] = users_loss[batchIdx] + loss
        users_val_loss[batchIdx] = users_val_loss[batchIdx] + val_loss

        new_weights.append(model.get_weights())

    return new_weights


def fedAvg(model, new_weights=[]):
    sum_weights = 0

    for i in range(0, len(new_weights)):
        sum_weights += np.array(new_weights[i], dtype=object)

    mean_weights = sum_weights / len(new_weights)

    model.set_weights(mean_weights.tolist())
    return model


def fl():
    avg_model = model

    for i in range(0, ROUND):
        print('\n')
        print('================Round' + str(i + 1) + '=================')

        new_weights = split_train(avg_model, dataset, test_imgs, test_labels)
        avg_model = fedAvg(model, new_weights)

        print('Evaluation')
        loss, acc = avg_model.evaluate(test_imgs, test_labels)

        overall_val_acc.append(acc)
        overall_val_loss.append(loss)

    for user in range(0, USER_NUM):
        plt.figure()
        plt.title("user" + str(user + 1) + " accuracy along rounds")
        plt.plot(users_acc[user], label='user_acc' + str(user + 1))
        plt.plot(users_val_acc[user], label='user_val_acc' + str(user + 1))
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.legend()
        plt.savefig('./ret_img/user' + str(user + 1) + '_acc.png')

        plt.figure()
        plt.title("user" + str(user + 1) + " loss along rounds")
        plt.plot(users_loss[user], label='user_loss' + str(user + 1))
        plt.plot(users_val_loss[user], label='user_val_loss' + str(user + 1))
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend()
        plt.savefig('./ret_img/user' + str(user + 1) + '_loss.png')

    plt.figure()
    plt.plot(overall_val_acc, label='overall accuracy')
    plt.xlabel('round')
    plt.ylabel('accuracy')
    plt.legend()
    plt.savefig('./ret_img/overall_acc.png')

    plt.figure()
    plt.plot(overall_val_loss, label='overall loss')
    plt.xlabel('round')
    plt.ylabel('loss')
    plt.legend()
    plt.savefig('./ret_img/overall_loss.png')


fl()
plt.show()
