import ipfshttpclient as ipfs
from web3 import Web3
import requests as rq


class ModelStorage:
    def __init__(self):
        self.client = ipfs.connect()

    def get_model(self, modelName):
        # directly get model from the local ipfs node
        return rq.get(f'http://localhost:8080/ipfs{modelName}')
        # return self.client.get_json(modelName)

    def store_model(self, model):
        # return the json hash
        return self.client.add_json(model)


model_storage = ModelStorage()
