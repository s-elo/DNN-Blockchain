from flask import Flask, jsonify, request
import requests
import time
import threading

app = Flask(__name__)

# every 10 seconds
TIME_SLOT = 10

clients = []


def main():
    while True:
        time.sleep(TIME_SLOT)

        if (len(clients) == 0):
            continue

        print(clients)
        for client in clients:
            resp = requests.post(client, json={'data': 'hello!'})

            print(resp.json())


@app.route('/<scriptName>')
def getModel(scriptName):
    client_addr = request.remote_addr
    client_port = request.args.get('port')

    print(client_addr, client_port)
    client_url = f'http://{client_addr}:{client_port}/'

    if client_url in clients:
        return jsonify(err=1, msg='you have already joined')

    clients.append(f'http://{client_addr}:{client_port}/')

    return jsonify(scriptName=scriptName, isDone=False)


if __name__ == '__main__':
    # creat a thread for schedule the training process and evaluation
    main_thread = threading.Thread(target=main)
    main_thread.start()

    # the main thread is for server listener
    app.run(host="0.0.0.0", port=5000, debug=True)
