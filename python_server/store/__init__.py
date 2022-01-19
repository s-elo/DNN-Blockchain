import ipfshttpclient as ipfs
from web3 import Web3
import requests as rq
from store.cifar10 import get_cifar10_model

intial_models = {
    'cifar10': get_cifar10_model
}


class ModelStorage:
    def __init__(self):
        self.client = ipfs.connect()

    # only need the struct ure of the model for server
    def get_model(self, modelName):
        return intial_models[modelName]()

        # directly get model from the local ipfs node
        # return rq.get(f'http://localhost:8080/ipfs{modelName}')
        # return self.client.get_json(modelName)

    def store_model(self, model):
        # return the json hash
        return self.client.add_json(model)


model_storage = ModelStorage()
