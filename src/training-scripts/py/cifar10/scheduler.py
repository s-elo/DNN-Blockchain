from typing import List
import threading
import time
import requests as rq
# from testset import get_testset
# from scheduler.utils import Utils
import numpy as np
import tensorflow as tf
# from store import model_storage as store


class Scheduler:
    def __init__(self) -> None:
        pass

    # implement the selection algro
    def node_selection(self, nodes):
        return nodes[len(nodes) - 1]

    # boardcast the params for all the other nodes
    def boardcast_params(self, node_addrs=[], params={}, delay=5):
        if (len(node_addrs) == 0):
            return []

        # for each node
        threads = []
        ret = [None]*len(node_addrs)

        def generate_req_fn(node_addr, idx):
            def req():
                resp = rq.post(node_addr, json=params)
                ret[idx] = resp

            return req

        # delay to boardcast
        time.sleep(delay)

        for idx, node_addr in enumerate(node_addrs):
            req_fn = generate_req_fn(node_addr, idx)

            th = threading.Thread(target=req_fn)
            th.start()
            threads.append(th)

        # until all the requests(threads) done
        for th in threads:
            th.join()

        return ret

    # first response than boardcast
    def async_boardcast(self, params={}, delay=3):
        boardcast_thread = threading.Thread(
            target=self.boardcast_params, args=(params, delay))
        boardcast_thread.start()

    def handle_boardcast_results(self, ret):
        pass
