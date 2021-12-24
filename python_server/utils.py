from typing import List
import socket
import threading
import time
import requests as rq


class DL:
    def __init__(self, applications: List[str], client_num, train_round) -> None:
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
    def boardcast_params(self, modelName, model={}, delay=5):
        client_list = self.clients[modelName]

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

    def handle_boardcast_results(self, ret):
        pass

    # first response than boardcast
    def async_boardcast(self, modelName, model={}, delay=5):
        boardcast_thread = threading.Thread(
            target=self.boardcast_params, args=(modelName, model, delay))
        boardcast_thread.start()

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
                'round': 1  # record how many rounds has joined
            })
            return False

    def add_round(self, modelName, client_url):
        client = self.get_client(modelName, client_url)

        if client != None:
            client['round'] = client['round'] + 1

    def get_client_num(self, modelName):
        return len(self.clients[modelName])

    def get_client(self, modelName, client_url):
        for client in self.clients[modelName]:
            if (client['client_url'] == client_url):
                return client

        return None

    def get_rounds(self, modelName, client_url):
        client = self.get_client(modelName, client_url)

        if client != None:
            return client['round']
        else:
            return 0

    # remove the model if it is done
    def is_done(self, modelName):
        print('evaluating the averaged params...')

    # see if the cilent has joined for {train_round} rounds
    def is_client_done(self, modelName, client_url):
        client = self.get_client(modelName, client_url)

        if client != None:
            return client['round'] == self.train_round
        else:
            return False

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
