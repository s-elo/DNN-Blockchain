from get_models.cifar10 import getModel
import tensorflow as tf


def get_model(modelName):
    if modelName == 'cifar10':
        model = getModel(input_shape=(32, 32, 3), kernel_size=3,
                         class_num=10, reg=True, normal=True)

        model.compile(optimizer=tf.keras.optimizers.Adam(),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    return None
