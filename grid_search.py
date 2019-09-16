#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: grid_search.py
@time: 2019-09-15 20:13
@desc:
'''


from music21 import *
from ACCO_PARSER.ACC_PARSER_SongWeight import SongParser_weight
from ACCO_PARSER.ACCO_PARSER_Song import SongParser
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_CNotes import CNotes
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_Chord import CChord
from ACCO_MODEL.ACCO_MODEL_SVMModel import SVCModel
from ACCO_MODEL.ACCO_MODEL_RandomForestModel import randomForstModel
from pandas.api.types import CategoricalDtype
from ACCO_MODEL.ACCO_MODEL_MLPClassifierModel import MLPModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn import linear_model
import sklearn.naive_bayes as nb
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


training_root = './ACCO_DATASET/training'
X = np.empty(shape=[0, 7])
y = np.empty(shape=[0, 1])
parser = SongParser()
filelist = os.listdir(training_root)
for file in filelist:
        melody, acco = parser.parser_midi_training(os.path.join(training_root, file))
        acco = parser.remove_header(acco)
        X_one, y_one = parser.parseSong(melody, acco)
        X, y = parser.training_join(X, X_one, y, y_one)

#model = RandomForestClassifier(min_samples_split=4, max_features='auto', criterion='gini', n_estimators=150)

training_data = np.hstack((X, y))
df = pd.DataFrame(training_data)
df.columns = ['head', 'tail', 'chord_inside', 'beat', 'longest', 'fre', 'first', 'chord']
cols = ['head', 'tail', 'chord_inside', 'beat', 'longest', 'fre', 'first']
for col in cols:
        df[col] = df[col].astype(int)
        df[col] = df[col].astype(str)

train_x = pd.get_dummies(df[cols])

X_train, X_test, y_train, y_test = train_test_split(train_x.values, y.reshape(-1, 1), test_size=0.25, random_state=33)
#model.fit(X_train, y_train)
#loss = model.score(X_test, y_test)
#model = SVC(kernel='rbf', C=30)
model = nb.GaussianNB()
parameters={}
grid = GridSearchCV(estimator=model, param_grid=parameters, cv=5)
grid.fit(X_train, y_train)
print(grid.best_score_)
print(grid.best_params_)