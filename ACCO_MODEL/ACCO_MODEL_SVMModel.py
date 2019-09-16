#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_MODEL_SVMModel.py
@time: 2019-08-22 22:37
@desc:
'''

import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler

class SVCModel:
    '''
    建立随机森林模型，用于训练和预测
    '''

    def __init__(self):
        self.__model = SVC(C=30, kernel='rbf')
        #self.__ss = StandardScaler()

    def train(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)
        self.__model.fit(X_train, y_train)
        loss = self.__model.score(X_test, y_test)
        #predict_y = self.__model.predict(X_test)
        #mae = mean_absolute_error(predict_y, y_test)
        #mse = mean_squared_error(predict_y, y_test)
        return loss

    def predict(self, X):
        predict_y = self.__model.predict(X)
        return np.mat(predict_y)

