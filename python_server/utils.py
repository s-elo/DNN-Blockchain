from typing import List
import socket
import threading
import time
import requests as rq


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


class DL:
    def __init__(self, applications: List[str]) -> None:
        self.utils = {
            'get_host_ip': get_host_ip,
        }

        self.clients = {}
        self.applications = applications
        # each model has multiple clients
        for m in self.applications:
            self.clients[m] = []

    # boardcast the corresponding model params for the application task
    def boardcast_params(self, application, params={}):
        client_list = self.clients[application]

        if (len(client_list) == 0):
            return []

        # for each client
        threads = []
        ret = [None]*len(client_list)

        def generate_req_fn(client_addr, idx):
            def req():
                resp = rq.post(client_addr, json=params)
                ret[idx] = resp

            return req

        for idx, addr in enumerate(client_list):
            req_fn = generate_req_fn(addr, idx)

            th = threading.Thread(target=req_fn)
            th.start()
            threads.append(th)

        # until all the requests(threads) done
        for th in threads:
            th.join()

        return ret

    def isContained(self, modelName, client_url):
        if client_url in self.clients[modelName]:
            return True
        else:
            return False

    def addClient(self, modelName, client_url):
        if (self.isContained(modelName, client_url)):
            return False
        else:
            self.clients[modelName].append(client_url)
            return True


if __name__ == '__main__':
    dl = DL()

    client_list = [
        'http://127.0.0.1:3250',
        'http://127.0.0.1:3250',
        'http://127.0.0.1:3250'
    ]

    ret = dl.boardcast_params(client_list, {'data': 'hello'})
    print(ret)
