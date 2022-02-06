from flask import Flask, jsonify, request
# import requests as rq
# import time
# import threading
from scheduler import Scheduler

CLIENT_NUM_LIMIT = 2
TRAIN_ROUND = 2
dl = Scheduler(['cifar10'], CLIENT_NUM_LIMIT, TRAIN_ROUND)

app = Flask(__name__)

# every 10 seconds
# TIME_SLOT = 10

nodes = {
    'cifar10': []
}


@app.route('/<modelName>', methods=['GET'])
# simulate getting the model from blockchain
def getModel(modelName):
    model = dl.models[modelName]['model']
    str_weights, str_model_structure = dl.utils.model_to_str(model)

    return jsonify(model={'params': str_weights, 'archi': str_model_structure})


@app.route('/<modelName>/nodes', methods=['GET'])
def getNodes(modelName):
    return jsonify(nodes=nodes[modelName])


@app.route('/<modelName>/nodes', methods=['POST'])
def addNodes(modelName):
    # exceed the maximum node number
    if CLIENT_NUM_LIMIT == len(nodes[modelName]):
        return jsonify(nodes=None)

    node_address = request.get_json()['address']

    nodes[modelName].append(node_address)

    return jsonify(nodes=nodes[modelName])


@app.route('/<modelName>', methods=['POST'])
def joinTraining(modelName):
    post_data = request.get_json()

    client_addr = request.remote_addr
    client_port = post_data['port']

    client_url = f'http://{client_addr}:{client_port}/'

    trained_model = {
        'params': post_data['params'],
        'archi': post_data['archi']
    }

    # add to the corresponding application model
    added_status = dl.add_client(modelName, client_url, trained_model)

    canAvg = dl.can_average(modelName)

    cur_round = dl.get_rounds(modelName, client_url)

    if added_status == 1:  # been added before
        # for next round
        if canAvg:
            print(f'avging the params of {modelName} for round {cur_round}...')
            avgModel = dl.fedAvg(modelName)

            print(f'evaluating the averaged model')
            dl.evaluate(modelName)

            # can average means all the clients are at the same round
            isDone = dl.is_client_done(modelName, client_url)

            if isDone:
                # tell all the cilents that is done
                # dl.async_boardcast(modelName, {'isDone': True, 'model': None})
                # since this must be the last done clients when canAvg
                dl.clear_clients(modelName)
                # store the model in ipfs
                # dl.store_model(avgModel)

                return jsonify(isFirstTime=False, isDone=True, needWait=False, round=cur_round)
            else:
                dl.async_boardcast(
                    modelName, {'model': avgModel})

                return jsonify(isFirstTime=False, isDone=False, needWait=False, round=cur_round)
        else:
            # see if this client has done all the rounds
            isDone = dl.is_client_done(modelName, client_url)
            # waiting for other clients to follow if it is not done
            return jsonify(isFirstTime=False, isDone=isDone, needWait=False if isDone else True, round=cur_round)
    elif added_status == 0:  # not been added before
        # first time join the training just for check without trained model
        # first time must be not done
        return jsonify(isFirstTime=True, canJoin=True, msg=f'joined the training of {modelName}')
    elif added_status == -1:  # reach maximum number
        return jsonify(isFirstTime=True, canJoin=False, msg=f'maximum client number is {dl.client_num}, you can join another time')


if __name__ == '__main__':
    # creat a thread for schedule the training process and evaluation
    # main_thread = threading.Thread(target=main)
    # main_thread.start()

    # the main thread is for server listener
    app.run(host="0.0.0.0", port=5000, debug=False)
