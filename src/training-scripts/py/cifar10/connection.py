from lib2to3.pytree import Node
import requests as rq
from web3 import Web3
import json
import os
import threading
from scheduler import Scheduler
from train import train
from dataHandler import load_split_train_data
import numpy as np

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
    def __init__(self, server_domain, server_port, self_port, modelName, data_set, node_num=2, total_round=2) -> None:
        super(Connector, self).__init__(
            self_port, modelName, node_num, total_round)

        self.server_domain = server_domain
        self.server_port = server_port

        self.server_addr = f'{server_domain}:{server_port}/{modelName}'
        self.ipfs_server_node = f'{server_domain}:{8080}/ipfs'

        self.data_set = data_set

    def check_model(self, from_ipfs=False):
        # request to join the training and get the model
        print(f'getting the mdoel from ipfs...')
        model = self.get_model(ipfs=from_ipfs)

        if model == None:
            print('seems the server/blockchain has a bit problem, try again next time')
            os._exit(0)

        self.model = model

        return model

    def get_model(self, ipfs=False):
        # get the model from server for simulation
        # it should actually get the model from blockchain (ipfs)
        if ipfs != True:
            model = rq.get(self.server_addr).json()['model']
        else:
            # model_hash = main_contract.functions.get().call()
            model_hash = 'QmUoPtUsFz5n98ycwGfcvCPTS16aZ42kiLmtx1nbnPoFgT'
            model = rq.get(f'{self.ipfs_server_node}/{model_hash}').json()

        return model

    def get_testset(self):
        print('loading the testset...')
        # it should from the blockchain based on the model name
        testset_hash = 'QmSHfdkQh3GG9JGaw2zihshNdm4nC29q4vp4d1pZKtHVCD'

        testset = rq.get(
            f'{self.ipfs_server_node}/{testset_hash}').json()

        return (np.array(testset['data']), np.array(testset['label']))

    def join_network(self):
        print(
            f'requesting to join the {self.modelName} current training network...')

        # it should fetch from the blockchain
        nodes = rq.post(f'{self.server_addr}/nodes', json={
            'address': self.address}).json()['nodes']

        # it means exceeding the maximum node number
        if nodes == None:
            print(
                f'Reached the maximum node number of the current training, please join next time.')
            os._exit(0)

        print(nodes)
        self.nodes = nodes

        if len(nodes) == self.total_node:
            # select the last node as the schedule node for the network and boardcast
            # except notify itself
            print('\n')
            print('You are the chosen one to average the models from other nodes!')
            self.test_data = self.get_testset()

            self.selected_node = self.address
            self.async_boardcast(router='node-selected', params={
                'node': self.node_selection(nodes)}, delay=2)

            # directly begin to train asyncly
            self.async_process_training()
        else:
            print(
                f'wait for {self.total_node - len(nodes)} more nodes to join...')

        # os._exit(0)

    def join_average(self, model_params: str, model_archi: str):
        if self.address == self.selected_node:
            # no need to post
            status = self.averge(
                new_model={'params': model_params, 'archi': model_archi})

            return status
        else:
            resp = rq.post(f'{self.selected_node}/join-average', json={
                'params': model_params, 'archi': model_archi, 'node': self.address})

            return resp.json()['status']

    def process_training(self):
        # os.environ['CUDA_VISIBLE_DEVICES'] = '1'
        if self.train_data == None:
            self.load_data(self.data_set)

        model = self.utils.str_to_model(
            self.model['params'], self.model['archi'])

        self.round = self.round + 1

        print(f'Training at round {self.round}')

        trained_model = train(model, self.train_data)

        print(f'training done for round {self.round}')

        str_params, str_archi = self.utils.model_to_str(trained_model)

        # request to join the averaging process
        status = self.join_average(str_params, str_archi)

        if status == 'WAITING':
            # the selected node will boardcast the averaged model
            # the selected node will wait for other nodes' new models
            print(
                f'wating for other nodes to train in round {self.round}...')
        elif status == 'AVERAGED':
            if self.isDone():
                print(f'{self.total_round} round training has completed.')
                # store the model in the ipfs
                self.utils.async_shutdown()
            else:
                if self.isSelected():
                    self.async_boardcast(router='get-model',
                                         params={'avgModel': self.model}, delay=2)

                    print('\n')
                    # continue to training
                    # the averaged model has been stored in self.model
                    self.process_training()
                else:
                    # the selected node will boardcast the averaged model
                    print(f'about to get the model for round {self.round + 1}')

    def async_process_training(self):
        training_thread = threading.Thread(
            target=self.process_training)
        training_thread.start()

    def isDone(self):
        return self.round == self.total_round

    def isSelected(self):
        return self.address == self.selected_node

    def load_data(self, data_set):
        # load the training dataset
        print('Loading training dataset...')
        dataset = load_split_train_data()

        self.train_data = dataset[data_set]
        print(
            f'Dataset loaded, find totally {self.train_data[0].shape[0]} data')
