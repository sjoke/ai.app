# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import metrics
import numpy as np

from random import randint
import matplotlib.pyplot as plt

import glob
import os
import urllib.request
import logging
import time


current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
# logging.basicConfig(filename='log/quickdraw_log_{}.log'.format(current_time), level=logging.INFO)

# output_file = open('log/quickdraw_log_{}.log'.format(current_time), 'w')
"""Download *.npz"""


def download():
    with open("class_names.txt", "r") as f:
        classes = f.readlines()
    base = 'https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/'
    for c in classes:
        cls_url = c.replace('_', '%20')
        path = base + cls_url + '.npy'
        print(path)
        urllib.request.urlretrieve(path, 'data/' + c + '.npy')

# download()


"""# Imports"""


def load_data(root, test_ratio=0.2, max_items_per_class=10000):
    all_files = glob.glob(os.path.join(root, '*.npy'))

    # initialize variables
    x = np.empty([0, 784])
    y = np.empty([0])
    class_names = []

    # load each data file
    for idx, file in enumerate(all_files):
        class_name = os.path.basename(file).split('.')[0].replace(' ', '_')
        class_names.append(class_name)

        data = np.load(file)
        # print('class[%s] has %d samples' % (class_name, data.shape[0]), file=output_file)
        data = data[0: max_items_per_class, :]
        labels = np.full(data.shape[0], idx)

        x = np.append(x, data, axis=0)
        y = np.append(y, labels)

    data = None
    labels = None

    # randomize the dataset
    permutation = np.random.permutation(y.shape[0])
    x = x[permutation, :]
    y = y[permutation]

    # separate into training and testing
    test_size = int(x.shape[0]/100*(test_ratio*100))

    x_test = x[0:test_size, :]
    y_test = y[0:test_size]

    x_train = x[test_size:, :]
    y_train = y[test_size:]
    return x_train, y_train, x_test, y_test, class_names

print('start to load data')
x_train, y_train, x_test, y_test, class_names = load_data('data', max_items_per_class=10000)
num_classes = len(class_names)
image_size = 28

print('num_classes: {}, x_train shape: {}'.format(num_classes, x_train.shape))
assert x_train.shape[0] == y_train.shape[0]
assert x_test.shape[0] == y_test.shape[0]


"""# Preprocess the Data"""

# Reshape and normalize
x_train = x_train.reshape(
    x_train.shape[0], image_size, image_size, 1).astype('float32')
x_test = x_test.reshape(
    x_test.shape[0], image_size, image_size, 1).astype('float32')

x_train /= 255.0
x_test /= 255.0

# Convert class vectors to class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


"""# The Model"""

# Define model
model = keras.Sequential()
model.add(layers.Convolution2D(64, (3, 3),
                               padding='same',
                               input_shape=(image_size, image_size, 1), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Convolution2D(128, (3, 3), padding='same', activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Convolution2D(256, (3, 3), padding='same', activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
# model.add(layers.Convolution2D(128, (3, 3), padding='same', activation='relu'))
# model.add(layers.MaxPooling2D(pool_size=(2, 2)))
# model.add(layers.Convolution2D(256, (3, 3), padding='same', activation='relu'))
# model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(num_classes, activation='softmax'))

print(model.summary())

# compile model
adam = tf.train.AdamOptimizer()

# top-N
TOP_N = 3

def top_n_categorical_accuracy(y_pred, y_label):
    return metrics.top_k_categorical_accuracy(y_pred, y_label, k=TOP_N)

model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=['accuracy', top_n_categorical_accuracy])

"""# Training"""

history = model.fit(x=x_train, y=y_train, validation_split=0.1,
                    batch_size=128, epochs=5)


"""# Testing"""

score = model.evaluate(x_test, y_test, verbose=0)

print('Test loss: {:.3f}, accurracy: {:.2f}%, top-{:d} accuarcy: {:0.2f}%'
      .format(score[0], score[1] * 100, TOP_N, score[2] * 100))

"""# Inference"""

model.save('quickDraw_{:.2f}percent.h5'.format(score[1] * 100))
