#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_MODEL_RandomForestModel.py
@time: 2019-08-22 22:22
@desc:
本项目目前采用的随机森林模型
'''

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler

class randomForstModel:
    '''
    建立随机森林模型，用于训练和预测
    '''

    def __init__(self):
        self.__model = RandomForestClassifier(min_samples_split=5, max_features='auto',
                                              criterion='gini', n_estimators=350)
        #self.__ss = StandardScaler()

    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=33)
        self.__model.fit(X_train, y_train)
        test_loss = self.__model.score(X_test, y_test)
        train_loss = self.__model.score(X_train, y_train)
        return test_loss, train_loss

    def predict(self, X):
        predict_y = self.__model.predict(X)
        return predict_y