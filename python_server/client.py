import requests as rq
from flask import Flask, request, jsonify
import time
import sys

SERVER_DOMAIN = 'http://localhost'
SERVER_PORT = '5000'

PORT = sys.argv[1] if len(sys.argv) >= 2 else '3250'

client = Flask(__name__)


resp = rq.get(f'{SERVER_DOMAIN}:{SERVER_PORT}/cifar10?port={PORT}').json()

print(resp)


@client.route('/', methods=['POST'])
def getMsg():
    data = request.get_json()

    print(data)

    return jsonify(
        get=True
    )


if __name__ == '__main__':
    client.run(host="0.0.0.0", port=PORT, debug=False)
