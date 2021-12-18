import time
import tensorflow as tf
import tensorflow_federated as tff

# Load simulation data.
source, _ = tff.simulation.datasets.emnist.load_data()


def client_data(n):
    return source.create_tf_dataset_for_client(source.client_ids[n]).map(
        lambda e: (tf.reshape(e['pixels'], [-1]), e['label'])
    ).repeat(10).batch(20)


print(len(source.client_ids))
# Pick a subset of client devices to participate in training.
train_data = [client_data(n) for n in range(3)]

# Grab a single batch of data so that TFF knows what data looks like.
element_spec = train_data[0].element_spec

# Wrap a Keras model for use with TFF.


def model_fn():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(10, tf.nn.softmax, input_shape=(784,),
                              kernel_initializer='zeros')
    ])
    return tff.learning.from_keras_model(
        model,
        input_spec=element_spec,
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])


# Simulate a few rounds of training with the selected client devices.
trainer = tff.learning.build_federated_averaging_process(
    model_fn,
    use_experimental_simulation_loop=True,
    client_optimizer_fn=lambda: tf.keras.optimizers.SGD(0.1))


def evaluate(num_rounds=10):
    state = trainer.initialize()
    for _ in range(num_rounds):
        # Pick a subset of client devices to participate in training.
        train_data = [client_data(n) for n in range(3)]
        t1 = time.time()
        state, metrics = trainer.next(state, train_data)
        t2 = time.time()
        print('metrics {m}, round time {t:.2f} seconds'.format(
            m=metrics['train'].items(), t=t2 - t1))


evaluate()


# OrderedDict([('broadcast', ()), ('aggregation', OrderedDict([('mean_value', ()), ('mean_weight', ())])), ('train', OrderedDict(
#     [('sparse_categorical_accuracy', 0.08109091), ('loss', 13.044773)])), ('stat', OrderedDict([('num_examples', 2750)]))])
