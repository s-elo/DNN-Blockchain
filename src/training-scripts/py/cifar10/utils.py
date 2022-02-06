import tensorflow as tf
from tensorflow.keras.models import model_from_json
import json
import numpy as np
import time
import threading
import os
import socket


def get_host_ip():
    """
    query IP address of current machine
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def model_to_str(model):
    # 1. stringify the weights
    weights = model.get_weights()

    str_weights = params_to_str(weights)

    # 2. stringify the structure of the model
    str_model_structure = model.to_json()

    return str_weights, str_model_structure


def str_to_model(str_weights, str_model_structure):
    weights = str_to_params(str_weights)

    model = str_to_structure(str_model_structure)

    model.set_weights(weights)

    return model


def str_to_params(str_weights):
    weights_info = json.loads(str_weights)

    weights = []
    for i in range(0, len(weights_info)):
        str_layer = weights_info[i]

        np_weights = np.frombuffer(
            bytes(str_layer['str']), dtype='float32').reshape(str_layer['shape'])

        weights.append(np_weights)

    return weights


def str_to_structure(str_model_structure):
    model = model_from_json(str_model_structure)

    return model


def params_to_str(params):
    weights_info = []
    for i in range(0, len(params)):
        # ndarray
        layer = params[i]

        # convert into bytes
        bytes_layer = layer.tobytes()

        weights_info.append({
            'str': list(bytes_layer),  # represented using int 0-255
            'shape': layer.shape,
            'type': str(layer.dtype)
        })

    str_weights = json.dumps(weights_info)

    return str_weights


def structure_to_str(model):
    return model.to_json()


def async_shutdown():
    def shutdown():
        time.sleep(2)
        os._exit(0)

    shutdown_thread = threading.Thread(target=shutdown)
    shutdown_thread.start()


class Utils:
    def __init__(self) -> None:
        self.str_to_model = str_to_model
        self.model_to_str = model_to_str
        self.str_to_params = str_to_params
        self.str_to_structure = str_to_structure
        self.params_to_str = params_to_str
        self.structure_to_str = structure_to_str
        self.async_shutdown = async_shutdown
        self.get_host_ip = get_host_ip


if __name__ == '__main__':
    print(get_host_ip())
