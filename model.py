#!/usr/bin/env python
# encoding: utf-8
'''
@author: Danniel
@license: (C) Copyright
@contact: 1085837135@qq.com
@software: PyCharm
@file: model.py
@time: 2019-04-10 17:33
@desc:
利用Keras创建的Model,训练和推断用model
'''

from keras.models import *
from keras.layers import *
from keras.initializers import glorot_uniform
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras import backend as K
from parser_midi.parser_grammar import *
from parser_midi.parser_midi import *
from parser_midi.parser_global import *
from parser_midi.parser_music import *
from music21 import *

'''
n_a = 64
reshapor = Reshape((1, 78))
LSTM_cell = LSTM(n_a, return_state=True)
densor = Dense(n_values, activation='softmax')
'''


def tranning_model(Tx, n_a, n_melody_values, n_acco_values, reshapor, LSTM_cell, densor):
    '''
    :param Tx:
    LSTM神经网络每个样本的输入个数，即输入序列的长度（时长）
    :param n_a:
    LSTM传递的参数
    :param n_melody_values
    输入的维度
    :param n_acco_values:
    输出的维度
    :param reshapor:
    调整输入的维度的模块
    :param LSTM_cell:
    训练的主要单元
    :param densor:
    输出单元
    :return:
    建立的一个模型(未训练)
    '''

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
    '''
    :param reshapor:
    调整输入维度
    :param LSTM_cell:
    训练后的单元
    :param densor:
    输出单元
    :param Tx:
    预测样本时序单元数目
    :param n_melody_values:
    主旋律表元素大小
    :param n_acco_values:
    伴奏表元素大小
    :param n_a:
    :param Ty:
    :return:
    '''

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