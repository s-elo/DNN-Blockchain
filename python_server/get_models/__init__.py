from get_models.cifar10 import getModel


def get_model(modelName):
    if modelName == 'cifar10':
        return getModel(input_shape=(32, 32, 3), kernel_size=3, class_num=10, reg=True, normal=True)

    return None
