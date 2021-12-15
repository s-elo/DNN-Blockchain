import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
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
BATCH_SIZE = 256
EPOCH = 100


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

    # fully connected layer 500 neurons
    model.add(layers.Dense(units=128, activation='relu'))

    model.add(layers.Dropout(0.5))
    
    # final fully connected layer CLASS_NUM neurons with respect to CLASS_NUM subjects
    model.add(layers.Dense(units=CLASS_NUM, activation='softmax',
              kernel_initializer='he_normal'))

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def train():
    gen = dataAugment(train_imgs, train_labels, batch_size=BATCH_SIZE)

    model = getModel()

    model.summary()

    log_dir = "./logs/fit/"

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir, histogram_freq=1)

    def scheduler(epoch, lr):
        if (epoch == 1):
            return 0.01
        if epoch % 10 == 0:
            return lr - 0.0005
        else:
            return lr

    learn_scheduler_callback = tf.keras.callbacks.LearningRateScheduler(
        scheduler)

    h = model.fit(x=gen,  epochs=EPOCH, steps_per_epoch=50000 // BATCH_SIZE,
                  validation_data=(test_imgs, test_labels), callbacks=[tensorboard_callback])
    # steps_per_epoch=50000//BATCH_SIZE

    # model.fit(train_imgs, train_labels, epochs=EPOCH, batch_size=BATCH_SIZE, shuffle=True,
    #           validation_data=(test_imgs, test_labels),
    #           callbacks=[tensorboard_callback])

    # model.save('CIFAR10_model_with_data_augmentation_dual_GPU.h5')
    # validation_data=(test_imgs, test_labels),


def dataAugment(x, y, batch_size=256):
    aug_gen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        # randomly rotate images in the range (degrees, 0 to 180)
        rotation_range=0,
        # randomly shift images horizontally (fraction of total width)
        width_shift_range=0.1,
        # randomly shift images vertically (fraction of total height)
        height_shift_range=0.1,
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False,  # randomly flip images
    )

    aug_gen.fit(x)
    gen = aug_gen.flow(x, y, batch_size=batch_size)

    return gen


train()
