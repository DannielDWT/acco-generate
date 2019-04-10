#!/usr/bin/env python
# encoding: utf-8
'''
@author: Danniel
@license: (C) Copyright
@contact: 1085837135@qq.com
@software: PyCharm
@file: parser_grammar.py
@time: 2019-04-03 20:17
@desc:
将字符串数据转换为数字数据
'''

import tensorflow as tf
import keras.backend as K
from keras.layers import RepeatVector
import sys
from music21 import *
import numpy as np

def parse_data(melody_corpus, acco_corpus, melody_val_indices,
                        acco_val_indices, m = 60, Tx = 30):
    '''
    :param melody_corpus:
    list类型，存储从头到尾的一个长串，依照时间顺序安排每个元素（主旋律）
    :param acco_corpus:
    list类型, 存储从头到尾的一个长串，依照时间顺序安排每个元素（伴奏）
    :param melody_val_indices:
    主旋律表
    :param acco_val_indices:
    伴奏表
    :param m:
    训练样本数
    :param Tx:
    训练输入数
    :return:
    返回样本数据和期望值
    '''
    #print(melody_corpus)
    #print(len(melody_corpus))
    N_acco_values = len(set(acco_corpus))
    N_melody_values = len(set(melody_corpus))
    np.random.seed()
    X = np.zeros((m, Tx, N_melody_values), dtype=np.bool)
    Y = np.zeros((m, Tx, N_acco_values), dtype=np.bool)
    for L in range(m):
        melody_offset = 0.0
        acco_offset = 0.0
        melody_random_idx = np.random.choice(450 -  Tx)
        melody_data = melody_corpus[melody_random_idx:melody_random_idx + Tx]
        for j in range(melody_random_idx):
            melody_terms = melody_corpus[j].split(',')
            offset = float(melody_terms[1])
            melody_offset += offset
        acco_idx = 0
        while acco_offset <= melody_offset:
            acco_terms = acco_corpus[acco_idx].split(',')
            offset = float(acco_terms[1])
            acco_offset += offset
            acco_idx += 1
            if (acco_idx == len(acco_corpus)):
                break
        for idx in range(Tx):
            melody_data_idx = melody_val_indices[melody_data[idx]]
            if acco_idx <= 0:
                acco_idx = 1
            acco_data_idx = acco_val_indices[acco_corpus[acco_idx - 1]]
            X[L, idx, melody_data_idx] = 1
            Y[L, idx, acco_data_idx] = 1
            melody_terms = melody_corpus[idx].split(',')
            offset = float(melody_terms[1])
            melody_offset += offset
            while acco_offset <= melody_offset:
                #print("acco: ", acco_offset)
                #print("melody: ", melody_offset)
                acco_terms = acco_corpus[acco_idx].split(',')
                offset = float(acco_terms[1])
                acco_offset += offset
                acco_idx += 1
                if (acco_idx == len(acco_corpus)):
                    break
    Y = np.swapaxes(Y, 0, 1)
    Y = Y.tolist()
    #print(X)
    return np.asarray(X), np.asarray(Y), N_melody_values, N_acco_values

def unparse_data(predict_indices, acco_indices_val):
    '''
    :param melody_corpus:
    list类型，包含依顺序放置的主旋律元素，字符串表达
    :param predict_indices:
    list类型，模型预测产生的数据集对应的索引，
    :param melody_indices_val:
    dict,用于获取对应的音符
    :param acco_indices_val:
    dict，用于获取对应的音符
    :return:
    list类型，伴奏的长字符串
    '''
    acco_corpus = []
    acco_offset = 0.0
    predict_indices_list = list(predict_indices)
    #print(predict_indices_list)
    indices = list(set(predict_indices_list))
    indices.sort(key=predict_indices_list.index)
    #print(indices)
    Y_len = len(indices)
    for L in range(Y_len):
        acco_terms = acco_indices_val[indices[L]].split(',')
        acco_corpus.append(acco_indices_val[indices[L]])
        acco_offset += float(acco_terms[1])
    if len(acco_corpus) == len(set(predict_indices)):
        print("yes")
    return acco_corpus




