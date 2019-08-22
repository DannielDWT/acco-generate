#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_MODEL_TF_IDF.py
@time: 2019-08-22 22:06
@desc:
'''


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_CNotes import CNotes

def tf_idf(X_train, X_test, features=CNotes.notes_num):
    '''
    :param X_train: 文本训练样本
    :param X_test: 文本测试集
    :param features: 返回的特征数目
    :return: 提取后的训练数据和测试数据
    采用TF-IDF提取文本特征
    '''

    vectorizer = CountVectorizer(max_features=features)
    tf_idf_transformer = TfidfTransformer()

    tf_idf = tf_idf_transformer.fit_transform(vectorizer.fit_transform(X_train))
    X_train_weight = tf_idf.toarray()

    tf_idf = tf_idf_transformer.transform(vectorizer.transform(X_test))
    X_test_weight = tf_idf.toarray()

    return X_train_weight, X_test_weight
