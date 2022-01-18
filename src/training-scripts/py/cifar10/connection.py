import requests as rq


class Connector:
    def __init__(self, server_domain, server_port, self_port, modelName) -> None:
        self.server_domain = server_domain
        self.server_port = server_port

        self.self_port = self_port
        self.modelName = modelName

        self.server_addr = f'{server_domain}:{server_port}/{modelName}'
        self.ipfs_server_node = f'{server_domain}:{8080}/ipfs/QmTdKW1bkQB5jjhd2cW8CghFzHzCZT8Mv7cGZdyqM5s4mm'
        self.round = 0

    def get_model(self):
        # get the model from server for simulation
        # it should actually get the model from blockchain (ipfs)
        # model = rq.get(self.server_addr).json()['model']

        model = rq.get(self.ipfs_server_node).json()

        return model

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
