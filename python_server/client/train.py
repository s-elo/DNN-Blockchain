import time
import threading
import os


def train(model):
    print(len(model['params']))
    time.sleep(5)
    return 'params', 'archi'


def async_shutdown():
    def shutdown():
        time.sleep(2)
        os._exit(0)

    shutdown_thread = threading.Thread(target=shutdown)
    shutdown_thread.start()


def process_training(model, connector):
    print(f'Training at round {connector.round + 1}')

    model_params, model_archi = train(model)

    print(f'training done for round {connector.round + 1}')
    status = connector.join_training(model_params, model_archi)

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
