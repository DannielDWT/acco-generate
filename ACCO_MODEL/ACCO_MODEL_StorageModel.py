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