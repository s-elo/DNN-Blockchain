from flask import Flask, request, jsonify
import time
import sys
import os
from connection import Connector
from dataHandler import load_split_train_data
import threading
ADDRESS = None

# it should be the ipfs node
SERVER_DOMAIN = 'http://localhost'
SERVER_PORT = '5000'

# default port is 3250
PORT = sys.argv[1] if len(sys.argv) >= 2 else '3250'

# default set is the first set
SET = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

MODEL_NAME = 'cifar10'

NODE_NUM = 2
ROUND = 2

if ADDRESS == None:
    ADDRESS = "0x8eacBB337647ea34eC26804C3339e80EB488587c"

dnn = Connector(SERVER_DOMAIN, SERVER_PORT, PORT,
                MODEL_NAME, SET, ADDRESS, NODE_NUM, ROUND)

# join the network
dnn.join_network()

node = Flask(__name__)


@node.route('/join-average', methods=['POST'])
# only for the selected node
def schedule():
    post_data = request.get_json()

    node = post_data['node']

    trained_model = {
        'params': post_data['params'],
        'archi': post_data['archi']
    }

    status = dnn.averge(new_model=trained_model)

    if status == 'AVERAGED':
        if dnn.isDone():
            print(f'{ROUND} round training has completed.')

            dnn.clearNodes()

            # store the model to ipfs

            # shutdown after returning the response
            dnn.utils.async_shutdown()
        else:
            dnn.async_boardcast(router='get-model',
                                params={'avgModel': dnn.model}, delay=2)
            # continue to training
            # the averaged model has been stored in self.model
            print('\n')
            dnn.async_process_training()

    return jsonify(status=status)


@node.route('/get-model', methods=['POST'])
def get_model():
    boardcast_data = request.get_json()

    model = boardcast_data['avgModel']

    # update the averaged model
    dnn.model = model

    print('\n')
    dnn.process_training()

    return jsonify(get=True)


@node.route('/node-selected', methods=['POST'])
def get_selected_node():
    dnn.selected_node = request.get_json()['node']
    print(f'selected node: {dnn.selected_node}')

    print('\n')
    # begin to train
    dnn.process_training()

    return jsonify(get=True)


node.run(host="0.0.0.0", port=PORT, debug=False)
