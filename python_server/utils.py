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
    def __init__(self, applications: List[str], client_num, train_round) -> None:
        self.utils = {
            'get_host_ip': get_host_ip,
        }

        # fiex value for each model
        self.client_num = client_num
        # fiex value for all model, each user has to do the number of this round
        self.train_round = train_round

        self.clients = {}
        self.applications = applications
        # each model has multiple clients
        for m in self.applications:
            self.clients[m] = []

    # boardcast the corresponding model params for the application task
    def boardcast_params(self, application, model={}, delay=5):
        client_list = self.clients[application]

        if (len(client_list) == 0):
            return []

        # for each client
        threads = []
        ret = [None]*len(client_list)

        def generate_req_fn(client_addr, idx):
            def req():
                resp = rq.post(client_addr, json=model)
                ret[idx] = resp

            return req

        # delay to boardcast
        time.sleep(delay)

        for idx, client in enumerate(client_list):
            req_fn = generate_req_fn(client['client_url'], idx)

            th = threading.Thread(target=req_fn)
            th.start()
            threads.append(th)

        # until all the requests(threads) done
        for th in threads:
            th.join()

        return ret

    def is_contained(self, modelName, client_url):
        if any(client['client_url'] == client_url for client in self.clients[modelName]):
            return True
        else:
            return False

    # return True to indicate it has been added
    def add_client(self, modelName, client_url, trained_model):
        if (self.is_contained(modelName, client_url)):
            # add the round
            self.add_round(modelName, client_url)
            return True
        else:
            self.clients[modelName].append({
                'client_url': client_url,
                'trained_model': trained_model,
                'round': 0  # record how many rounds has joined
            })
            return False

    def add_round(self, modelName, client_url):
        clients = self.clients[modelName]
        for client in clients:
            if client['client_url'] == client_url:
                client['round'] = client['round'] + 1
                return

    def get_client_num(self, modelName):
        return len(self.clients[modelName])

    def is_done(self, modelName):
        print('evaluating the averaged params...')

    # each client must be at the train_round
    # only called after calling can_average, which means all the clients have the same round
    def is_client_done(self, modelName):
        return self.clients[modelName][0]['round'] == self.train_round

    # check if the averaging condition is met
    def can_average(self, modelName):
        # 1. the number of joined clients must be 5
        if (self.get_client_num(modelName) != self.client_num):
            return False

        clients = self.clients[modelName]

        # 2. the rounds of each client must be the same
        bench_value = clients[0]['round']
        for client in clients:
            if (client['round'] != bench_value):
                return False

        return True

    def clear_clients(self, modelName):
        self.clients[modelName] = []


if __name__ == '__main__':
    arr = [{'a': 1}, {'a': 3}]

    def c(x):
        return (x['a'] == 5)

    print(any(x['a'] == 3 for x in arr))
