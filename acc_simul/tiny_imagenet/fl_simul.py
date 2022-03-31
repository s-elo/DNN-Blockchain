import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from dataHandler import load_numpy_data, dataAugment, batch_size, class_num, height, width, channels
from model import getModel, get_pretrained_model
import shutil
import os
from checkpoint import Checkpoint

if os.path.exists('./ret_img') == True:
    shutil.rmtree('./ret_img')
os.mkdir('./ret_img')

ROUND = 15
USER_NUM = 5
EPOCHS = 20

print('Loading data...')
x_train, y_train, x_test, y_test = load_numpy_data()
# split the training data
dataset = list(zip(np.split(x_train, USER_NUM, axis=0),
               np.split(y_train, USER_NUM, axis=0)))
print('Data loaded.')
print(len(dataset), dataset[0][0].shape, dataset[0][1].shape)

tf.random.set_seed(2345)

global_info = Checkpoint(ROUND, USER_NUM)

start_round, users_acc, users_val_acc, users_loss, users_val_loss, overall_acc, overall_loss, overall_val_acc, overall_val_loss = global_info.start()

# reducing learning rate on plateau
rlrop = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss', mode='min', patience=5, factor=0.5, min_lr=1e-6, verbose=1)


def split_train(model, dataset, test_imgs, test_labels):
    weights = model.get_weights()

    new_weights = []
    for batchIdx in range(0, len(dataset)):
        print('\n')
        print('================User' + str(batchIdx + 1) + '=================')

        train_imgs = dataset[batchIdx][0]
        train_labels = dataset[batchIdx][1]

        print(train_imgs.shape)
        gen = dataAugment(train_imgs, train_labels, batch_size=batch_size)

        # get another model instance to avoid multiple memory allocations when compiling
        # model = get_pretrained_model((height, width, channels), class_num)
        model = getModel((height, width, channels), kernel_size=3,
                         class_num=class_num, reg=True, normal=True)
        model.set_weights(weights)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        h = model.fit(x=gen,  epochs=EPOCHS, steps_per_epoch=len(train_imgs) // batch_size, batch_size=batch_size,
                      validation_data=(test_imgs, test_labels), callbacks=[rlrop])

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
    cur_round = start_round
    # model = getModel(test_imgs.shape[1:], KERNEL_SIZE, CLASS_NUM)
    # model = get_pretrained_model((height, width, channels), class_num)
    model = getModel((height, width, channels), kernel_size=3,
                     class_num=class_num, reg=True, normal=True)
    if cur_round != 1:
        model.load_weights('./weights/avg_weights')

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()

    avg_model = model

    while cur_round <= ROUND:
        print('\n')
        print('================Round' + str(cur_round) + '=================')

        new_weights = split_train(avg_model, dataset, x_test, y_test)
        avg_model = fedAvg(model, new_weights)

        print('Evaluation')
        loss, acc = avg_model.evaluate(x_train, y_train)
        val_loss, val_acc = avg_model.evaluate(x_test, y_test)

        overall_acc.append(acc)
        overall_loss.append(loss)
        overall_val_acc.append(val_acc)
        overall_val_loss.append(val_loss)

        cur_round = cur_round + 1

        # save the checkpoint for this round
        global_info.save_weights(avg_model)
        global_info.save_per_round(
            cur_round, users_acc, users_val_acc, users_loss, users_val_loss, overall_acc, overall_loss, overall_val_acc, overall_val_loss)

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
    plt.title('merged model accuracy per round')
    plt.plot(overall_acc, label='merged model train accuracy')
    plt.plot(overall_val_acc, label='merged model test accuracy')
    plt.xlabel('round')
    plt.ylabel('accuracy')
    plt.legend()
    plt.savefig('./ret_img/overall_acc.png')

    plt.figure()
    plt.title('merged model loss per round')
    plt.plot(overall_loss, label='merged model train loss')
    plt.plot(overall_val_loss, label='merged model test loss')
    plt.xlabel('round')
    plt.ylabel('loss')
    plt.legend()
    plt.savefig('./ret_img/overall_loss.png')

    # remove the checkpoints
    global_info.remove()


fl()
plt.show()
