from flask import Flask, jsonify, request
import requests as rq
import time
import threading
from utils import DL

CLIENT_NUM_LIMIT = 2
TRAIN_ROUND = 2
dl = DL(['cifar10'], CLIENT_NUM_LIMIT, TRAIN_ROUND)

app = Flask(__name__)

# every 10 seconds
TIME_SLOT = 10

# simulate getting the model from blockchain


@app.route('/<modelName>', methods=['GET'])
def get_model(modelName):
    return jsonify(model=modelName)


@app.route('/<modelName>', methods=['POST'])
def join_training(modelName):
    post_data = request.get_json()

    client_addr = request.remote_addr
    client_port = post_data['port']

    client_url = f'http://{client_addr}:{client_port}/'

    trained_model = {
        'params': post_data['params'],
        'archi': post_data['archi']
    }

    # add to the corresponding application model
    beenAdded = dl.add_client(modelName, client_url, trained_model)

    canAvg = dl.can_average(modelName)

    if beenAdded:
        # for next round
        if canAvg:
            print('avging the params')
            isDone = dl.is_client_done(modelName)
            time.sleep(5)

            if isDone:
                # tell all the cilents that is done
                dl.boardcast_params(modelName, {'isDone': True, 'model': None})

                dl.clear_clients(modelName)

                return jsonify(err=0, isDone=True, needWait=False)
            else:
                dl.boardcast_params(
                    modelName, {'model': 'avgModel', 'isDone': False})

                return jsonify(err=0, isDone=False, needWait=False)
        else:
            # waiting for other clients to follow
            return jsonify(err=0, isDone=False, needWait=True)
    else:
        # first time join the training
        if canAvg:
            print('avging the params')
            time.sleep(5)

            dl.boardcast_params(
                modelName, {'model': 'avgModel', 'isDone': False})
            # first time must be not done
            return jsonify(err=0, isDone=False, needWait=False)
        else:
            return jsonify(err=0, isDone=False, needWait=True)


if __name__ == '__main__':
    # creat a thread for schedule the training process and evaluation
    # main_thread = threading.Thread(target=main)
    # main_thread.start()

    # the main thread is for server listener
    app.run(host="0.0.0.0", port=5000, debug=False)
