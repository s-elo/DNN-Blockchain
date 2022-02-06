from lib2to3.pytree import Node
import requests as rq
from web3 import Web3
import json
import os
from scheduler import Scheduler

apiKey = 'ab53629910c440089fda82f82af645f7'
w3 = Web3(Web3.HTTPProvider(
    f'https://ropsten.infura.io/v3/{apiKey}'))


def read(path='./contract.json'):
    with open(path, 'r') as load_f:
        return json.load(load_f)


contract_info = read(path='./contract.json')
contractAddress = contract_info['address']
abi = contract_info['abi']
main_contract = w3.eth.contract(contractAddress, abi=abi)


class Connector(Scheduler):
    def __init__(self, server_domain, server_port, self_port, modelName, node_num=2, total_round=2) -> None:
        super(Connector, self).__init__()

        self.nodes = []
        self.selected_node = None
        self.self_node = None

        self.server_domain = server_domain
        self.server_port = server_port

        self.self_port = self_port
        self.modelName = modelName

        self.server_addr = f'{server_domain}:{server_port}/{modelName}'
        self.ipfs_server_node = f'{server_domain}:{8080}/ipfs'

        self.total_node = node_num
        self.total_round = total_round
        self.round = 0

    def check_model(self, from_ipfs=False):
        # request to join the training and get the model
        print(f'getting the mdoel from ipfs...')
        model = self.get_model(ipfs=from_ipfs)

        if model == None:
            print('seems the server/blockchain has a bit problem, try again next time')
            os._exit(0)

        return model

    def get_model(self, ipfs=False):
        # get the model from server for simulation
        # it should actually get the model from blockchain (ipfs)
        if ipfs != True:
            model = rq.get(self.server_addr).json()['model']
        else:
            model_hash = main_contract.functions.get().call()

            model = rq.get(f'{self.ipfs_server_node}/{model_hash}').json()

        return model

    def join_network(self):
        # it should fetch from the blockchain
        nodes = rq.post(f'{self.server_addr}/nodes', json={
            'port': self.self_port}).json()['nodes']

        print(nodes)
        self.nodes = nodes
        # the last one should be the address of this current node
        self.self_node = nodes[len(nodes) - 1]

        if len(nodes) < self.total_node:
            # less than the required node number, need waiting
            print(
                f'wait for {self.total_node - len(nodes)} more nodes to join...')
        else:
            # select the last node as the schedule node for the network and boardcast
            # except notify itself
            self.selected_node = self.self_node
            rets = self.boardcast_params(node_addrs=self.filter_self(), params={
                                         'node': self.node_selection(nodes)}, delay=1)

            self.handle_boardcast_results(rets)

        # os._exit(0)

    def join_training(self, model_params: str, model_archi: str):
        """
        return 
        - 0: waiting
        - 1: done
        - -1: request wrong
        - 2: not done no waiting (get average model)
        - -2: client number overflow, can not join
        - 3: can join
        """
        print(f'requesting to join the {self.modelName} training...')

        # request to join the training process
        resp = rq.post(self.server_addr, json={
                       'params': model_params, 'archi': model_archi, 'port': self.self_port})

        # check the status
        if (resp.status_code == 200):
            json_data = resp.json()

            if (json_data['isFirstTime'] == False):
                self.round = json_data['round']

                if (json_data['isDone']):
                    return 1
                else:
                    if json_data['needWait']:
                        return 0
                    else:
                        return 2
            else:
                print(json_data['msg'])
                return (3 if json_data['canJoin'] else -2)
        else:
            return -1

    def filter_self(self):
        return list(map(
            lambda node: f'{node}/node-selected', self.nodes))[0:self.total_node - 1]
