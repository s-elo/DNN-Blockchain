from privateKey import private_key
from web3 import Web3
import json


def read(path='./contract.json'):
    with open(path, 'r') as load_f:
        return json.load(load_f)


class Contract:
    def __init__(self, account_address) -> None:
        self.account_address = account_address

        apiKey = 'ab53629910c440089fda82f82af645f7'
        self.w3 = Web3(Web3.HTTPProvider(
            f'https://ropsten.infura.io/v3/{apiKey}'))

        contract_info = read(path='./contract.json')
        contractAddress = contract_info['address']
        abi = contract_info['abi']
        self.contract = self.w3.eth.contract(contractAddress, abi=abi)

    def getNodes(self):
        nodes = self.contract.functions.getNodes().call()

        return nodes

    def addNode(self, node_address):
        self.callMethod('addNode', node_address)

    def clearNodes(self):
        self.callMethod('clearNodes')

    def update_model(self, model_name, model_hash):
        self.callMethod('updateModel', model_name, model_hash)

    def update_testset(self, model_name, testset_hash):
        self.callMethod('updateTestset', model_name, testset_hash)

    # for blockchain state-imutate functions
    def callMethod(self, method, *args):
        nonce = self.w3.eth.get_transaction_count(
            self.account_address)

        # {
        #     'chainId': 1,
        #     'gas': 70000,
        #     'maxFeePerGas': w3.toWei('2', 'gwei'),
        #     'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        #     'nonce': nonce,
        # }
        builded_txn = self.contract.functions[method](
            *args).buildTransaction({'nonce': nonce})

        signed_txn = self.w3.eth.account.sign_transaction(
            builded_txn, private_key=private_key)

        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return self.w3.eth.wait_for_transaction_receipt(tx_hash)
