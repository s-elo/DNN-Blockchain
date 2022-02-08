import tensorflow as tf
from tensorflow.keras.models import model_from_json
import json
import numpy as np


def model_to_str(model):
    # 1. stringify the weights
    weights = model.get_weights()

    weights_info = []
    for i in range(0, len(weights)):
        # ndarray
        layer = weights[i]

        # convert into bytes
        bytes_layer = layer.tobytes()

        weights_info.append({
            'str': list(bytes_layer),  # represented using int 0-255
            'shape': layer.shape,
            'type': str(layer.dtype)
        })

    str_weights = json.dumps(weights_info)

    # 2. stringify the structure of the model
    str_model_structure = model.to_json()

    return str_weights, str_model_structure


def str_to_model(str_weights, str_model_structure):
    weights_info = json.loads(str_weights)

    weights = []
    for i in range(0, len(weights_info)):
        str_layer = weights_info[i]

        np_weights = np.frombuffer(
            bytes(str_layer['str']), dtype='float32').reshape(str_layer['shape'])

        weights.append(np_weights)

    model = model_from_json(str_model_structure)

    model.set_weights(weights)

    return model
