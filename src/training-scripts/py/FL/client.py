import os

import flwr as fl
import tensorflow as tf

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
# Make TensorFlow log less verbose
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

print(__name__)
if __name__ == "__main__":
    # Load and compile Keras model
    model = tf.keras.applications.MobileNetV2(
        (32, 32, 3), classes=10, weights=None)
    model.compile("adam", "sparse_categorical_crossentropy",
                  metrics=["accuracy"])

    # Load CIFAR-10 dataset
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

    # Define Flower client
    class CifarClient(fl.client.NumPyClient):
        def get_parameters(self):  # type: ignore
            return model.get_weights()

        def fit(self, parameters, config):  # type: ignore
            model.set_weights(parameters)
            h = model.fit(x_train, y_train, epochs=1, batch_size=32)

            ret = {
                "loss": h.history["loss"][0],
                "accuracy": h.history["accuracy"][0],
            }
            return model.get_weights(), len(x_train), ret

        def evaluate(self, parameters, config):  # type: ignore
            model.set_weights(parameters)
            print('evaluating:\n')
            loss, accuracy = model.evaluate(x_test, y_test)
            return loss, len(x_test), {"accuracy": accuracy}

    # Start Flower client
    fl.client.start_numpy_client("0.0.0.0:8080", client=CifarClient())
