from get_models.cifar10 import get_cifar10_model
import tensorflow as tf


def get_model(modelName, isInital=False):
    if modelName == 'cifar10':
        return get_cifar10_model(isInital=isInital)

    return None
