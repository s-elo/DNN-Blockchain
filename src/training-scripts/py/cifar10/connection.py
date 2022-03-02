import requests as rq
import os
import threading
from scheduler import Scheduler
from train import train
from dataHandler import load_remote
import numpy as np
from contract import Contract


class Connector(Scheduler):
    def __init__(self, server_domain, server_port, self_port, modelName, data_set, account_address, node_num=2, total_round=2) -> None:
        super(Connector, self).__init__(
            self_port, modelName, node_num, total_round)

        self.account_address = "0x8eacBB337647ea34eC26804C3339e80EB488587c" if account_address == None else account_address

        self.server_domain = server_domain
        self.server_port = server_port

        self.server_addr = f'{server_domain}:{server_port}/{modelName}'
        self.ipfs_server_node = f'{server_domain}:{8080}/ipfs'

        self.data_set = data_set

        self.contract = Contract(account_address)

    def check_model(self):
        # request to join the training and get the model
        print(f'getting the mdoel from ipfs...')
        model = self.get_model()

        if model == None:
            print('seems the server/blockchain has a bit problem, try again next time')
            os._exit(0)

        self.model = model

        return model

    def get_model(self):
        # get the model from server for simulation
        # it should actually get the hash from blockchain (ipfs)
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

    def getNodes(self):
        # it should fetch from the blockchain
        # nodes = rq.post(f'{self.server_addr}/nodes', json={
        #     'address': self.address}).json()['nodes']
        nodes = self.contract.getNodes()

        return nodes

    def addNode(self):
        try:
            self.contract.addNode(self.address)
        except ValueError:
            print('One node is joining, please wait a minute to join again')
            os._exit(0)

    def clearNodes(self):
        # clear the ip address asyncly
        thread = threading.Thread(
            target=self.contract.clearNodes)
        thread.start()
        # receipt = callMethod(main_contract, 'clearNodes')
        # print(receipt)

    def join_network(self):
        print(
            f'requesting to join the {self.modelName} current training network...')

        nodes = self.getNodes()

        # it means exceeding the maximum node number
        if len(nodes) >= self.total_node and (self.address not in nodes):
            # see if this node has joined before but somehow exit
            print(
                f'Reached the maximum node number of the current training, please join next time.')
            os._exit(0)

        if self.address not in nodes:
            self.addNode()
            # after adding successfully
            nodes.append(self.address)
            print(nodes)

        # get the model and check if it exists
        self.check_model()

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

                if self.isSelected():
                    self.clearNodes()

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
        dataset = load_remote(split_num=self.total_node)

        self.train_data = dataset[data_set]
        print(
            f'Dataset loaded, find totally {self.train_data[0].shape[0]} data')


if __name__ == '__main__':
    sc = Contract("0x8eacBB337647ea34eC26804C3339e80EB488587c")
    receipt = sc.clearNodes()
    print('cleared')
