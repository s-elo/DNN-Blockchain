from flask import Flask, jsonify, request
import requests as rq
import time
import threading
from utils import DL

dl = DL(['cifar10'])

app = Flask(__name__)

# every 10 seconds
TIME_SLOT = 10


def main():
    while True:
        time.sleep(TIME_SLOT)

        resp = dl.boardcast_params(
            application='cifar10', params={'data': 'hello'})

        # it means no client
        if (len(resp) == 0):
            continue

        print(resp)


@app.route('/<modelName>', methods=['GET'])
def join_training(modelName):
    client_addr = request.remote_addr
    client_port = request.args.get('port')

    print(client_addr, client_port)
    client_url = f'http://{client_addr}:{client_port}/'

    # add to the corresponding application model
    isAdded = dl.addClient(modelName, client_url)

    if isAdded:
        return jsonify(scriptName=modelName, isDone=False)
    else:
        return jsonify(err=1, msg='you have already joined')


if __name__ == '__main__':
    # creat a thread for schedule the training process and evaluation
    main_thread = threading.Thread(target=main)
    main_thread.start()

    # the main thread is for server listener
    app.run(host="0.0.0.0", port=5000, debug=False)
