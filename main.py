# the main script for training the net on the count_lsts of titles - which are mapped to to scores

import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os
import json

from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy

# fix random seed for reproducibility
numpy.random.seed(7)
1
2
3
4
5
from keras.models import Sequential
from keras.layers import Dense

def train():
    # load the data
    print("Generating Train Label Data")
    with open("train_db.json") as train_db:
        # create a dict to map ids to class
        title_to_ups = json.load(train_db)
        x_train = []
        y_train = []
        for title, score in title_to_ups.items():
            x_train.append(np.array(eval(title)))
            y_train.append( score)
    
    
    # populate test ids
    print("Generating Test Label Data")
    with open("test_db.json") as test_db:
        # create a dict to map ids to class
        # create a dict to map ids to class
        title_to_ups = json.load(test_db)
        x_test = []
        y_test = []
        for title, score in title_to_ups.items():
            x_test.append(np.array(eval(title)))
            y_test.append( score)
    
    x_train = np.array(x_train)
    x_test = np.array(x_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    # sanity check
    print(len(x_train))
    print(len(x_test))

    # print(x_train[1000], y_train[1000])


    # ++++++++++++++++++
    num_inputs = len(x_train[0])
    num_outputs = 4
    # ++++++++++++++++++


    # create model
    model = Sequential()
    model.add(Dense(32, input_dim=542, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(16, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(8, activation='sigmoid'))
    model.add(Dropout(0.1))
    model.add(Dense(num_outputs, activation='sigmoid'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=150, batch_size=20)
    # evaluate the model
    scores = model.evaluate(x_test, y_test)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

if __name__ == "__main__":
    train()