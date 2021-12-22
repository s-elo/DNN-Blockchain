import requests as rq
from flask import Flask, request, jsonify
import time
from utils import get_host_ip

SERVER_DOMAIN = 'http://localhost'
SERVER_PORT = '5000'

client = Flask(__name__)


# resp = rq.get(f'{SERVER_DOMAIN}:{SERVER_PORT}/cifar10?port=3250').json()

# print(resp)


@client.route('/', methods=['POST'])
def getMsg():
    data = request.get_json()

    print(data)

    return jsonify(
        get=True
    )


if __name__ == '__main__':
    client.run(host="0.0.0.0", port=3250, debug=True)
