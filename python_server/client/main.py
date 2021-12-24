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
    print('seems the server/blockchain has a bit problem')
    os._exit()
else:
    print(f'get model {model}')


def process_training(model):
    print(model)
    model_params, model_archi = train(model)

    status = connector.join_training(model_params, model_archi)

    if status == 0:
        # the server will boardcast
        print('just wating...')
    elif status == 1:
        print('done training')
    elif status == -1:
        print('request wrong... just wait')
    elif status == 2:
        # the server will boardcast
        print('about to get the model')


# execute for the first time
train_process_thread = threading.Thread(target=process_training, args=(model,))
train_process_thread.start()

client = Flask(__name__)


@client.route('/', methods=['POST'])
def get_boardcast():
    boardcast_data = request.get_json()

    isDone = boardcast_data['isDone']

    if isDone:
        # os._exit()
        print('shut down...')
        return jsonify(isShutDown=True)

    model = boardcast_data['model']

    print('\n')
    process_training(model)

    return jsonify(
        get=True
    )


client.run(host="0.0.0.0", port=PORT, debug=False)
