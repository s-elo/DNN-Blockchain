import requests as rq
from flask import Flask, request, jsonify
import time
import sys
import os
from connection import Connector
from train import process_training
import threading

SERVER_DOMAIN = 'http://localhost'
SERVER_PORT = '5000'

# default port is 3250
PORT = sys.argv[1] if len(sys.argv) >= 2 else '3250'

modelName = 'cifar10'

connector = Connector(SERVER_DOMAIN, SERVER_PORT, PORT, modelName)

# request to join the training and get the model
model = connector.get_model()

if model == None:
    print('seems the server/blockchain has a bit problem, try again next time')
    os._exit(0)

# check if can be joined
status = connector.join_training(None, None)
if status == -2:  # can not join, join next time
    time.sleep(2)
    os._exit(0)

# execute for the first time
train_process_thread = threading.Thread(
    target=process_training, args=(model, connector))
train_process_thread.start()


client = Flask(__name__)


@client.route('/', methods=['POST'])
def get_boardcast():
    boardcast_data = request.get_json()

    model = boardcast_data['model']

    print('\n')
    process_training(model, connector)

    return jsonify(
        get=True
    )


client.run(host="0.0.0.0", port=PORT, debug=False)
