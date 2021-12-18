import nest_asyncio
import collections
import numpy as np
import tensorflow as tf
import tensorflow_federated as tff
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

nest_asyncio.apply()

np.random.seed(0)

# print(tff.federated_computation(lambda: 'Hello, World!')())
emnist_train, emnist_test = tff.simulation.datasets.emnist.load_data()

print(len(emnist_train.client_ids))
print(emnist_train.element_type_structure)

# one of the clients
example_dataset = emnist_train.create_tf_dataset_for_client(
    emnist_train.client_ids[0])

print(type(example_dataset))

example_element = next(iter(example_dataset))
example_element['label'].numpy()
print(example_element['label'].numpy())

NUM_CLIENTS = 10
NUM_EPOCHS = 5
BATCH_SIZE = 20
SHUFFLE_BUFFER = 100
PREFETCH_BUFFER = 10


def preprocess(dataset):

    def batch_format_fn(element):
        """Flatten a batch `pixels` and return the features as an `OrderedDict`."""
        return collections.OrderedDict(
            x=tf.reshape(element['pixels'], [-1, 784]),
            y=tf.reshape(element['label'], [-1, 1]))

    return dataset.repeat(NUM_EPOCHS).shuffle(SHUFFLE_BUFFER, seed=1).batch(
        BATCH_SIZE).map(batch_format_fn).prefetch(PREFETCH_BUFFER)


def make_federated_data(client_data, client_ids):
    return [
        preprocess(client_data.create_tf_dataset_for_client(x))
        for x in client_ids
    ]


sample_clients = emnist_train.client_ids[0:NUM_CLIENTS]

federated_train_data = make_federated_data(emnist_train, sample_clients)

print('Number of client datasets: {l}'.format(l=len(federated_train_data)))
print('First dataset: {d}'.format(d=federated_train_data[0]))


def create_keras_model():
    return tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(784,)),
        tf.keras.layers.Dense(10, kernel_initializer='zeros'),
        tf.keras.layers.Softmax(),
    ])


preprocessed_example_dataset = preprocess(example_dataset)


def model_fn():
    # We _must_ create a new model here, and _not_ capture it from an external
    # scope. TFF will call this within different graph contexts.
    keras_model = create_keras_model()
    return tff.learning.from_keras_model(
        keras_model,
        input_spec=preprocessed_example_dataset.element_spec,
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])


iterative_process = tff.learning.build_federated_averaging_process(
    model_fn,  # it is a constructor, not an instance
    use_experimental_simulation_loop=True,  # multiple GPU
    client_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=0.02),
    server_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=1.0))


# print(str(iterative_process.initialize.type_signature))
# SERVER_STATE, FEDERATED_DATA -> SERVER_STATE, TRAINING_METRICS
logdir = "./logs/scalars/training/"
summary_writer = tf.summary.create_file_writer(logdir)

state = iterative_process.initialize()

NUM_ROUNDS = 11

with summary_writer.as_default():
    for round_num in range(1, NUM_ROUNDS):
        state, metrics = iterative_process.next(state, federated_train_data)
        print('round {:2d}, metrics={}'.format(round_num, metrics))
        for name, value in metrics['train'].items():
            tf.summary.scalar(name, value, step=round_num)
