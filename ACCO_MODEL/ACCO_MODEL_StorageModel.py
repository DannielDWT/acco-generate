#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_MODEL_StorageModel.py
@time: 2019-08-20 10:41
@desc:
'''

'''

def tranning_model(Tx, n_a, n_melody_values, n_acco_values, reshapor, LSTM_cell, densor):

    # Define the input of your model with a shape
    X = Input(shape=(Tx, n_melody_values))

    # Define s0, initial hidden state for the decoder LSTM
    a0 = Input(shape=(n_a,), name='a0')
    c0 = Input(shape=(n_a,), name='c0')
    a = a0
    c = c0

    outputs = []

    for t in range(Tx):
        x = Lambda(lambda x: X[:, t, :])(X)
        x = reshapor(x)
        a, _, c = LSTM_cell(x, initial_state=[a, c])
        out = densor(a)
        outputs.append(out)

    # Create model instance
    model = Model(inputs=[X, a0, c0], outputs=outputs)

    return model


def predict_model(reshapor, LSTM_cell, densor, Tx,  n_melody_values, n_acco_values, n_a=64):

    # Define the input of your model with a shape
    X = Input(shape=(Tx, n_melody_values))

    # Define s0, initial hidden state for the decoder LSTM
    a0 = Input(shape=(n_a,), name='a0')
    c0 = Input(shape=(n_a,), name='c0')
    a = a0
    c = c0

    outputs = []

    # Loop over Ty and generate a value at every time step
    for t in range(Tx):
        x = Lambda(lambda x: X[:, t, :])(X)
        x = reshapor(x)
        a, _, c = LSTM_cell(x, initial_state=[a, c])
        out = densor(a)
        outputs.append(out)

    # Create model instance with the correct "inputs" and "outputs"
    inference_model = Model(inputs=[X, a0, c0], outputs=outputs)

    return inference_model
'''

'''
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.metrics import classification_report, mean_absolute_error, mean_squared_error
# 该标准化是对列数据/特征进行归一/标准化
#from sklearn.preprocessing import StandardScaler

class MLPModel:

    建立神经网络（多层感知机）分类模型，用于训练和预测


    def __init__(self):
        self.__model = MLPClassifier(hidden_layer_sizes=(10, 10), activation='relu', solver='lbfgs',
                                     alpha=1e-5, max_iter=190, random_state=33)
        #隐层个数可以考虑7  * 7 或者单层14或49， 如果是组合特征的话 单层考虑7或者10或者14
        #self.__ss = StandardScaler()

    def train(self, X, y):
        #ss = StandardScaler()
        #X_processed = ss.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
        self.__model.fit(X_train, y_train)
        training_loss = self.__model.score(X_train, y_train)
        loss = self.__model.score(X_test, y_test)
        #print(X_test)
        #print(y_test)
        #print(self.__model.predict(X_test))
        score = accuracy_score(y_test, self.__model.predict(X_test))
        #predict_y = self.__model.predict(X_test)
        #mae = mean_absolute_error(predict_y, y_test)
        #mse = mean_squared_error(predict_y, y_test)
        return loss

    def predict(self, X):
        predict_y = self.__model.predict(X)
        return np.mat(predict_y)
'''