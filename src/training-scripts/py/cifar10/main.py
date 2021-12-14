import tensorflow as tf
from tensorflow.keras import layers, models
# from tensorflow.keras.datasets import cifar10
# from tensorflow.keras.utils import to_categorical
from dataHandler import load_data, CLASS_NUM

print('Loading data...')
train_imgs, train_labels = load_data(type='TRAIN')
test_imgs, test_labels = load_data(type='TEST')
# (train_imgs, train_labels), (test_imgs, test_labels) = cifar10.load_data()

# train_labels = train_labels.reshape(train_labels.shape[0])
# test_labels = test_labels.reshape(test_labels.shape[0])

# print('X_train shape:', train_imgs.shape)
# print(train_imgs.shape[0], 'training samples')
# print(test_imgs.shape[0], 'validation samples')

# train_imgs = train_imgs.astype('float32')
# test_imgs = test_imgs.astype('float32')
# train_imgs /= 255
# test_imgs /= 255

# train_labels = to_categorical(train_labels, CLASS_NUM)
# test_labels = to_categorical(test_labels, CLASS_NUM)

print('Data loaded.')
# print(train_imgs[0:1], train_labels.shape)

KERNEL_SIZE = 3


def getModel():
    model = models.Sequential()

    # stage 1
    model.add(layers.Conv2D(filters=64, strides=1, kernel_size=KERNEL_SIZE, activation='relu',
                            input_shape=train_imgs.shape[1:], kernel_initializer='he_normal', padding='same'))

    model.add(layers.Conv2D(filters=64, strides=1, kernel_size=KERNEL_SIZE, activation='relu',
                            kernel_initializer='he_normal', padding='same'))

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # stage 2
    model.add(layers.Conv2D(filters=128, strides=1, kernel_size=KERNEL_SIZE, activation='relu',
                            kernel_initializer='he_normal', padding='same'))

    model.add(layers.Conv2D(filters=128, strides=1, kernel_size=KERNEL_SIZE, activation='relu',
                            kernel_initializer='he_normal', padding='same'))

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # stage 3
    model.add(layers.Conv2D(filters=256, strides=1, kernel_size=KERNEL_SIZE, activation='relu',
                            kernel_initializer='he_normal', padding='same'))

    model.add(layers.Conv2D(filters=256, strides=1, kernel_size=KERNEL_SIZE, activation='relu',
                            kernel_initializer='he_normal', padding='same'))

    model.add(layers.MaxPooling2D(pool_size=2, strides=2, padding='same'))

    # flatten as one dimension
    model.add(layers.Flatten())

    model.add(layers.Dropout(0.5))

    # fully connected layer 500 neurons
    # model.add(layers.Dense(500, activation='relu'))

    # final fully connected layer 26 neurons with respect to 26 subjects
    model.add(layers.Dense(CLASS_NUM, activation='softmax',
              kernel_initializer='he_normal'))

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def train():
    model = getModel()

    model.summary()

    log_dir = "./logs/fit/"
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir, histogram_freq=1)

    model.fit(train_imgs, train_labels, epochs=100, batch_size=256, shuffle=True,
              validation_data=(test_imgs, test_labels), callbacks=[tensorboard_callback])


train()
