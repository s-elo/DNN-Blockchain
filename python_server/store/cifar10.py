import os
from tensorflow.keras import layers, models
import tensorflow as tf
import requests as rq

os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


def get_model(input_shape, kernel_size, class_num, reg=True, normal=True):
    model = models.Sequential()

    # stage 1
    model.add(layers.Conv2D(filters=64, strides=1, kernel_size=kernel_size, activation='relu',
                            input_shape=input_shape, kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters=64, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # stage 2
    model.add(layers.Conv2D(filters=128, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters=128, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # stage 3
    model.add(layers.Conv2D(filters=256, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.Conv2D(filters=256, strides=1, kernel_size=kernel_size, activation='relu',
                            kernel_initializer='he_normal', padding='same'))
    if (normal):
        model.add(layers.BatchNormalization())

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # flatten as one dimension
    model.add(layers.Flatten())

    # fully connected layer 500 neurons
    model.add(layers.Dense(units=128, activation='relu',
              kernel_regularizer='l2' if reg else None))

    model.add(layers.Dropout(0.5))

    # final fully connected layer CLASS_NUM neurons with respect to CLASS_NUM subjects
    model.add(layers.Dense(units=class_num, activation='softmax',
              kernel_initializer='he_normal', kernel_regularizer='l2' if reg else None))

    return model


def get_cifar10_model():
    model = get_model(input_shape=(32, 32, 3), kernel_size=3,
                      class_num=10, reg=True, normal=True)

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model
    # get from ipfs
    # else:
    #     model = model_storage.get_model(
    #         'QmTdKW1bkQB5jjhd2cW8CghFzHzCZT8Mv7cGZdyqM5s4mm')


if __name__ == '__main__':
    from web3 import Web3
    import json
    from privateKey import key
    import ipfshttpclient as ipfs
    from utils import model_to_str

    print('web3 test here')

    def save(path='./data.json', data=[]):
        with open(path, "w") as f:
            json.dump(data, f)
            print("加载入文件完成...")

    def read(path='./data.json'):
        with open(path, 'r') as load_f:
            data = json.load(load_f)

            return data

    model = get_cifar10_model(isInital=True)

    # model.save('./model.h5')

    str_params, str_archi = model_to_str(model)

    print(len(str_params), len(str_archi))

    data = {'params': str_params, 'archi': str_archi}

    # save(data=data)

    apiKey = 'ab53629910c440089fda82f82af645f7'

    w3 = Web3(Web3.HTTPProvider(
        f'https://ropsten.infura.io/v3/{apiKey}'))

    print(w3.isConnected())

    balance = w3.eth.get_balance('0x8eacBB337647ea34eC26804C3339e80EB488587c')

    print(balance)

    contract_info = read(path='./contract.json')

    contractAddress = contract_info['address']

    abi = contract_info['abi']

    resp = rq.get(
        f'https://api-ropsten.etherscan.io/api?module=contract&action=getabi&address={contractAddress}')

    print(resp)

    w3.eth.default_account = '0x8eacBB337647ea34eC26804C3339e80EB488587c'
    w3.eth.account.from_key(key)

    contract = w3.eth.contract(contractAddress, abi=abi)

    def callMethod(contract, method, *args):
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
            builded_txn, private_key=key)

        return w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # tx_hash = callMethod(contract, 'set', 'alterstring')
    # print(tx_hash)

    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)

    string = contract.functions.get().call()
    print(string)

    # client = ipfs.connect()
    # pin_list = client.pin.ls(type='all')
    # print(pin_list['Keys']['QmTdKW1bkQB5jjhd2cW8CghFzHzCZT8Mv7cGZdyqM5s4mm'])
    # print(len(client.get_json(
    #     'QmTdKW1bkQB5jjhd2cW8CghFzHzCZT8Mv7cGZdyqM5s4mm')['params']))
    # model_hash = client.add_json(data)

    # model_hash = 'QmTdKW1bkQB5jjhd2cW8CghFzHzCZT8Mv7cGZdyqM5s4mm'
    # print(model_hash)

    # print(client.cat('QmfXT9rNL5rnvHv3yy1di5nrAdNPXfv7re7t4xGE6yXUod'))
    # resp = rq.get(f'http://localhost:8080/ipfs/{model_hash}')

    # print(len(resp.json()['params']))
