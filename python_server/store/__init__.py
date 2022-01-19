import ipfshttpclient as ipfs
from web3 import Web3
import requests as rq
import json
from store.cifar10 import get_cifar10_model
from store.privateKey import private_key

intial_models = {
    'cifar10': get_cifar10_model
}

apiKey = 'ab53629910c440089fda82f82af645f7'
w3 = Web3(Web3.HTTPProvider(
    f'https://ropsten.infura.io/v3/{apiKey}'))


def save(path='./store/contract.json', data=[]):
    with open(path, "w") as f:
        json.dump(data, f)


def read(path='./store/contract.json'):
    with open(path, 'r') as load_f:
        return json.load(load_f)


contract_info = read()
contractAddress = contract_info['address']
abi = contract_info['abi']
main_contract = w3.eth.contract(contractAddress, abi=abi)


class ModelStorage:
    def __init__(self):
        self.client = ipfs.connect()
        self.contract = main_contract

    # only need the struct ure of the model for server
    def get_initial_model(self, modelName):
        # for test, initial the model params for the blockchain
        # everytime reboot the server

        # unpin the previous one
        # prev_model_hash = self.contract.functions.get().call()
        # self.client.pin.rm(prev_model_hash)

        tx_hash = self.callMethod(
            main_contract, 'set', 'QmTdKW1bkQB5jjhd2cW8CghFzHzCZT8Mv7cGZdyqM5s4mm')
        # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return intial_models[modelName]()

        # directly get model from the local ipfs node
        # return rq.get(f'http://localhost:8080/ipfs{modelName}')
        # return self.client.get_json(modelName)

    def store_model(self, model):
        model_hash = self.client.add_json(model)

        self.callMethod(main_contract, 'set', model_hash)

        # record the hash been used
        self.store_model_hash(model_hash)

        return model_hash

    def callMethod(self, contract, method, *args):
        nonce = w3.eth.get_transaction_count(
            '0x8eacBB337647ea34eC26804C3339e80EB488587c')

        # {
        #     'chainId': 1,
        #     'gas': 70000,
        #     'maxFeePerGas': w3.toWei('2', 'gwei'),
        #     'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        #     'nonce': nonce,
        # }
        builded_txn = contract.functions[method](
            *args).buildTransaction({'nonce': nonce})

        signed_txn = w3.eth.account.sign_transaction(
            builded_txn, private_key=private_key)

        return w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    def store_model_hash(self, model_hash):
        hash_arr = read(path='./store/model_hash.json')

        hash_arr.append(model_hash)

        save(path='./store/model_hash.json', data=hash_arr)


model_storage = ModelStorage()
