#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_MODEL_BayesModel.py
@time: 2019-08-19 16:57
@desc:
'''

from sklearn.model_selection import train_test_split
import sklearn.naive_bayes as nb
import numpy as np
from sklearn.metrics import classification_report, mean_absolute_error, mean_squared_error
# 该标准化是对列数据/特征进行归一/标准化
#from sklearn.preprocessing import StandardScaler

class multinomiaModel:
    '''
    建立朴素贝叶斯分类模型，多项式分布朴素贝叶斯模型，用于训练和预测
    '''

    def __init__(self):
        self.__model = nb.MultinomialNB()
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


class gaussianModel:
    '''
    建立朴素贝叶斯分类模型，高斯分布朴素贝叶斯模型，用于训练和预测
    '''

    def __init__(self):
        self.__model = nb.GaussianNB()

    def train(self, X, y):
        X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.23, random_state=33)
        self.__model.fit(X_train, y_train)
        loss = self.__model.score(X_test, y_test)
        return loss

    def predict(self, X):
        predict_y = self.__model.predict(X)
        return np.mat(predict_y)