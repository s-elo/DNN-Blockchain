import requests as rq
import os


class Connector:
    def __init__(self, server_domain, server_port, self_port, application) -> None:
        self.server_addr = server_domain
        self.server_port = server_port

        self.self_port = self_port
        self.application = application

        self.server_addr = f'{server_domain}:{server_port}/{application}'
        self.round = 1

    def get_model(self):
        # get the model from server for simulation
        # it should actually get the model from blockchain
        model = rq.get(self.server_addr).json()['model']
        return model

    def join_training(self, model_params, model_archi):
        """
        return 
        - 0: waiting
        - 1: done
        - -1: request wrong
        - 2: not done no waiting (get average model)
        """
        print(f'requesting to join the {self.application} training...')

        # request to join the training process
        resp = rq.post(self.server_addr, json={
                       'params': model_params, 'archi': model_archi, 'port': self.self_port})

        # check the status
        if (resp.status_code == 200):
            json_data = resp.json()

            if (json_data['err'] == 0):
                self.round = json_data['round']

                if (json_data['isDone']):
                    return 1
                else:
                    if json_data['needWait']:
                        return 0
                    else:
                        return 2
        else:
            return -1
