from numpy import number
from flask import Flask, request, jsonify
import time
import sys
import os
from connection import Connector
from train import process_training, train
from dataHandler import load_split_train_data
import threading
from model import getModel
from modelStorage import str_to_model, model_to_str

SERVER_DOMAIN = 'http://localhost'
SERVER_PORT = '5000'

# default port is 3250
PORT = sys.argv[1] if len(sys.argv) >= 2 else '3250'

MODEL_NAME = 'cifar10'

connector = Connector(SERVER_DOMAIN, SERVER_PORT, PORT, MODEL_NAME)

# request to join the training and get the model
# model_ = connector.get_model()
# print(len(model_['params']), len(model_['archi']))
# if model_ == None:
#     print('seems the server/blockchain has a bit problem, try again next time')
#     os._exit(0)

model = getModel(input_shape=(32, 32, 3), kernel_size=3,
                 class_num=10, reg=True, normal=True)
p, a = model_to_str(model)
model = {
    'params': p,
    'archi': a
}
# # check if can be joined
status = connector.join_training(None, None)
if status == -2:  # can not join, join next time
    time.sleep(2)
    os._exit(0)

# load the training dataset
print('Loading training dataset...')
dataset = load_split_train_data()
# default set is the first set
SET = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

train_data = dataset[SET]
print(f'Dataset loaded, find totally {train_data[0].shape[0]} data')

# os.environ['CUDA_VISIBLE_DEVICES'] = '1'
# os.environ['CUDA_VISIBLE_DEVICES'] = sys.argv[3] if len(sys.argv) >= 4 else '0'

# execute for the first time
train_process_thread = threading.Thread(
    target=process_training, args=(model, train_data, connector))
train_process_thread.start()


client = Flask(__name__)


@client.route('/', methods=['POST'])
def get_boardcast():
    boardcast_data = request.get_json()

    model = boardcast_data['model']

    print('\n')
    process_training(model, train_data, connector)

    return jsonify(
        get=True
    )


client.run(host="0.0.0.0", port=PORT, debug=False)
