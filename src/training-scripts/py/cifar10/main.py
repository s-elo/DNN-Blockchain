from flask import Flask, request, jsonify
import time
import sys
import os
from connection import Connector
from train import process_training
from dataHandler import load_split_train_data
import threading

SERVER_DOMAIN = 'http://localhost'
SERVER_PORT = '5000'

# default port is 3250
PORT = sys.argv[1] if len(sys.argv) >= 2 else '3250'

MODEL_NAME = 'cifar10'

NODE_NUM = 3
ROUND = 2

from_ipfs = False

dnn = Connector(SERVER_DOMAIN, SERVER_PORT, PORT,
                MODEL_NAME, NODE_NUM, ROUND)

model = dnn.check_model(from_ipfs=from_ipfs)

# join the network
dnn.join_network()

# # check if can be joined
# status = connector.join_training(None, None)
# if status == -2:  # can not join, join next time
# time.sleep(2)
# os._exit(0)

# load the training dataset
# print('Loading training dataset...')
# dataset = load_split_train_data()
# # default set is the first set
# SET = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

# train_data = dataset[SET]
# print(f'Dataset loaded, find totally {train_data[0].shape[0]} data')

# # execute for the first time
# train_process_thread = threading.Thread(
#     target=process_training, args=(model, train_data, dnn))
# train_process_thread.start()


node = Flask(__name__)


@node.route('/', methods=['POST'])
def get_boardcast():
    boardcast_data = request.get_json()

    model = boardcast_data['model']

    print('\n')
    # process_training(model, train_data, dnn)

    return jsonify(
        get=True
    )


@node.route('/node-selected', methods=['POST'])
def get_selected_node():
    dnn.selected_node = request.get_json()['node']
    print(f'selected node: {dnn.selected_node}')

    return jsonify(get=True)


node.run(host="0.0.0.0", port=PORT, debug=False)
