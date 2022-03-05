import requests as rq
from contract import Contract
from accounts import accounts
from config import MODEL_NAME

if type(accounts).__name__ == 'list':
    # use the first one by default
    address = accounts[0]['address']
    private_key = accounts[0]['private_key']
else:
    address = accounts['address']
    private_key = accounts['private_key']

contract = Contract(account_address=address,
                    modelName=MODEL_NAME, private_key=private_key)

# get the model hash from blockchain
print('getting the model hash from blockchain...')
model_hash = contract.getModelHash()
# fetch the model
print('fetching the model from ipfs...')
res = rq.get(f'https://{model_hash}.ipfs.dweb.link/{MODEL_NAME}_model.json')

if res.status_code == 200:
    l = len(res.json()['params'])
    print(f'loaded! the model length is {l}')
else:
    print('something went wrong, please try again')
