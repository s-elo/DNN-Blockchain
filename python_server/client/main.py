import requests as rq
from flask import Flask, request, jsonify
import time
import sys
import os
from connection import Connector
from train import train
import threading

SERVER_DOMAIN = 'http://localhost'
SERVER_PORT = '5000'

PORT = sys.argv[1] if len(sys.argv) >= 2 else '3250'

application = 'cifar10'

connector = Connector(SERVER_DOMAIN, SERVER_PORT, PORT, application)

# request to join the training and get the model
model = connector.get_model()

if model == None:
    print('seems the server/blockchain has a bit problem, try again next time')
    os._exit(0)


def process_training(model):
    model_params, model_archi = train(model)

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


# execute for the first time
train_process_thread = threading.Thread(target=process_training, args=(model,))
train_process_thread.start()


def async_shutdown():
    def shutdown():
        time.sleep(5)
        os._exit(0)

    shutdown_thread = threading.Thread(target=shutdown)
    shutdown_thread.start()


client = Flask(__name__)


@client.route('/', methods=['POST'])
def get_boardcast():
    boardcast_data = request.get_json()

    model = boardcast_data['model']

    print('\n')
    process_training(model)

    return jsonify(
        get=True
    )


client.run(host="0.0.0.0", port=PORT, debug=False)
