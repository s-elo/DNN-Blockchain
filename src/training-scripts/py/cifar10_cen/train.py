import time
import threading
import os
from utils import str_to_model, model_to_str
from dataHandler import dataAugment
import tensorflow as tf


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


BATCH_SIZE = 64
EPOCH = 2


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


def async_shutdown():
    def shutdown():
        time.sleep(2)
        os._exit(0)

    shutdown_thread = threading.Thread(target=shutdown)
    shutdown_thread.start()


def process_training(model, train_data, connector):
    # os.environ['CUDA_VISIBLE_DEVICES'] = '1'

    model = str_to_model(model['params'], model['archi'])

    print(f'Training at round {connector.round + 1}')

    trained_model = train(model, train_data)

    print(f'training done for round {connector.round + 1}')

    str_params, str_archi = model_to_str(trained_model)

    # request to join the averaging process
    status = connector.join_training(str_params, str_archi)

    if status == 0:
        # the server will boardcast
        print(f'wating for other clients to train round {connector.round}...')
    elif status == 1:
        print('done training')
        async_shutdown()
        print('shutting down...')

    elif status == -1:
        print('request wrong... just wait')
    elif status == 2:
        # the server will boardcast
        print(f'about to get the model for round {connector.round + 1}')
    elif status == -2:
        # info printed during join_training function
        async_shutdown()
        print('shutting down...')
