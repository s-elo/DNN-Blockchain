import json
import os
import shutil

check_path = './check_info.json'


def save(data=[], path=check_path):
    with open(path, "w") as f:
        json.dump(data, f)


def read(path=check_path):
    with open(path, 'r') as load_f:
        return json.load(load_f)


class Checkpoint:
    def __init__(self, total_round=10, user_num=5) -> None:
        self.round = total_round
        self.user_num = user_num
        if os.path.exists(check_path) == True:
            self.check_info = read()
        else:
            self.check_info = {
                'round': 1,
                'users_acc': [[]]*self.user_num,
                'users_val_acc': [[]]*self.user_num,
                'users_loss': [[]]*self.user_num,
                'users_val_loss': [[]]*self.user_num,
                'overall_acc': [[]]*self.round,
                'overall_loss': [[]]*self.round,
                'overall_val_acc': []*self.round,
                'overall_val_loss': []*self.round
            }

            # create a new checkpoint file and save the initial values
            open(check_path, 'w').close()
            save(self.check_info)

    # check where to start
    def start(self):
        return (
            self.check_info['round'],
            self.check_info['users_acc'],
            self.check_info['users_val_acc'],
            self.check_info['users_loss'],
            self.check_info['users_val_loss'],
            self.check_info['overall_acc'],
            self.check_info['overall_loss'],
            self.check_info['overall_val_acc'],
            self.check_info['overall_val_loss']
        )

    def save_weights(self, model):
        print('saving weights...')
        if os.path.exists('./weights') == True:
            shutil.rmtree('./weights')

        os.mkdir('./weights')

        model.save_weights('./weights/avg_weights')
        print('saved')

    def save_per_round(self, cur_round, users_acc, users_val_acc, users_loss, users_val_loss, overall_acc, overall_loss, overall_val_acc, overall_val_loss):
        print('saving round info...')

        save(data={
            'round': cur_round,
            'users_acc': users_acc,
            'users_val_acc': users_val_acc,
            'users_loss': users_loss,
            'users_val_loss': users_val_loss,
            'overall_acc': overall_acc,
            'overall_loss': overall_loss,
            'overall_val_acc': overall_val_acc,
            'overall_val_loss': overall_val_loss
        })
        print('saved')

    def remove(self):
        os.remove(check_path)
        shutil.rmtree('./weights')
