import threading
import time
import requests as rq
# from testset import get_testset
from utils import Utils
import numpy as np
from train import evaluate


class Scheduler:
    def __init__(self, self_port, modelName, node_num, total_round) -> None:
        self.utils = Utils()

        self.nodes = []
        self.selected_node = None
        self.address = f'http://{self.utils.get_host_ip()}:{self_port}/'

        self.modelName = modelName

        self.total_node = node_num
        self.total_round = total_round
        self.round = 0

        self.train_data = None
        self.test_data = None

        # for current node training
        self.model = None

        # store for later averaging
        self.models = []

    def avg_check(self):
        # 1. the number of models must be euqal to the required node number
        if (len(self.models) != self.total_node):
            return False

        return True

    def averge(self, new_model):
        self.models.append(new_model)

        canAvg = self.avg_check()

        if canAvg:
            print('averaging the models...')
            self.fedAvg()

            self.evaluate()

            # clear for next round
            self.models = []

            return 'AVERAGED'
        else:
            return 'WAITING'

    def fedAvg(self):
        sum_weights = 0

        for model in self.models:
            weights = self.utils.str_to_params(model['params'])

            sum_weights += np.array(weights, dtype=object)

        mean_weights = (sum_weights / len(self.models)).tolist()

        self.model['params'] = self.utils.params_to_str(mean_weights)

     # evaluate the accuracy of a certain model
    def evaluate(self):
        print(f'\nEvaluating the averaged model...')
        model = model = self.utils.str_to_model(
            self.model['params'], self.model['archi'])

        evaluate(model, self.test_data)

    # implement the selection algro
    def node_selection(self, nodes):
        return nodes[len(nodes) - 1]

    # boardcast the params for all the other nodes
    def boardcast_params(self, router='', params={}, delay=5):
        nodes = self.filter_self(router=router)

        if (len(nodes) == 0):
            return []

        # for each node
        threads = []
        ret = [None]*len(nodes)

        def generate_req_fn(node_addr, idx):
            def req():
                resp = rq.post(node_addr, json=params)
                ret[idx] = resp

            return req

        # delay to boardcast
        time.sleep(delay)

        for idx, node_addr in enumerate(nodes):
            req_fn = generate_req_fn(node_addr, idx)

            th = threading.Thread(target=req_fn)
            th.start()
            threads.append(th)

        # until all the requests(threads) done
        for th in threads:
            th.join()

        return ret

    # first response than boardcast
    def async_boardcast(self, router='', params={}, delay=3):
        boardcast_thread = threading.Thread(
            target=self.boardcast_params, args=(router, params, delay))
        boardcast_thread.start()

    def handle_boardcast_results(self, ret):
        pass

    def filter_self(self, router=''):
        return list(map(
            lambda node: f'{node}/{router}', filter(lambda node: node != self.address, self.nodes)))
