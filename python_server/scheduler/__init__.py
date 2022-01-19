from typing import List
import threading
import time
import requests as rq
from testset import get_testset
from scheduler.utils import Utils
import numpy as np
import tensorflow as tf
from store import model_storage as store


class Scheduler:
    def __init__(self, modelNames: List[str], client_num, train_round) -> None:
        self.utils = Utils()

        # fiex value for each model
        self.client_num = client_num
        # fiex value for all model, each user has to do the number of this round
        self.train_round = train_round

        self.clients = {}
        self.models = {}

        self.modelNames = modelNames

        self.store = store

        for m in self.modelNames:
            # each model has multiple clients
            self.clients[m] = []

            model_info = {
                'testset': get_testset(m),
                # get compiled model (only need the structure actually)
                'model': store.get_initial_model(m)
            }

            self.models[m] = model_info

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
    def async_boardcast(self, modelName, model={}, delay=3):
        boardcast_thread = threading.Thread(
            target=self.boardcast_params, args=(modelName, model, delay))
        boardcast_thread.start()

    def is_contained(self, modelName, client_url):
        if any(client['client_url'] == client_url for client in self.clients[modelName]):
            return True
        else:
            return False

    # return True to indicate it has been added
    def add_client(self, modelName, client_url, trained_model=None):
        """
        return:
        - -1: can not be added, reach maximum number of clients
        - 0: not been added before, and added
        - 1: added before, no need added, but increment the round
        """
        if (self.is_contained(modelName, client_url)):
            # add the round
            self.add_round(modelName, client_url)
            self.update_model(modelName, client_url, trained_model)
            return 1
        else:
            if (self.get_client_num(modelName) == self.client_num):
                return -1

            self.clients[modelName].append({
                'client_url': client_url,
                'trained_model': trained_model,
                # record how many rounds has joined
                # 0 means just for check without providing trained model (None)
                'round': 0
            })
            return 0

    def add_round(self, modelName, client_url):
        client = self.get_client(modelName, client_url)

        if client != None:
            client['round'] = client['round'] + 1

    def update_model(self, modelName, client_url, trained_model):
        client = self.get_client(modelName, client_url)

        if client != None:
            client['trained_model'] = trained_model

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

    # remove the model if it is done (accuracy is reached certain point)
    def is_model_done(self, modelName):
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

    def store_model(self, model):
        model_hash = store.store_model(model)

        print(model_hash)

    # evaluate the accuracy of a certain model
    def evaluate(self, modelName):
        test_x, test_y = self.models[modelName]['testset']

        model = self.models[modelName]['model']

        model.evaluate(test_x, test_y)

    def fedAvg(self, modelName):
        clients = self.clients[modelName]

        sum_weights = 0

        for client in clients:
            client_model = client['trained_model']

            weights = self.utils.str_to_params(client_model['params'])

            sum_weights += np.array(weights, dtype=object)

        mean_weights = (sum_weights / len(clients)).tolist()

        model = self.models[modelName]['model']
        model.set_weights(mean_weights)

        return {
            'params': self.utils.params_to_str(mean_weights),
            'archi': self.utils.structure_to_str(model)
        }


if __name__ == '__main__':
    arr = [{'a': 1}, {'a': 3}]

    def c(x):
        return (x['a'] == 5)

    print(any(x['a'] == 3 for x in arr))
