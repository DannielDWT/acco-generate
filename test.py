#!/usr/bin/env python
# encoding: utf-8
'''
@author: Danniel
@license: (C) Copyright
@contact: 1085837135@qq.com
@software: PyCharm
@file: test.py
@time: 2019-04-01 19:41
@desc:
用于项目创建过程中的测试文件
2019-09-21 by danniel 注释掉测试内容，文件保留
'''

'''
from music21 import *
from ACCO_PARSER.ACCO_PARSER_Song import SongParser
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_CNotes import CNotes
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_Chord import CChord
from ACCO_MODEL.ACCO_MODEL_SVMModel import SVCModel
from ACCO_MODEL.ACCO_MODEL_DescionTree import DecisionTreeModel
from ACCO_MODEL.ACCO_MODEL_RandomForestModel import randomForstModel
from pandas.api.types import CategoricalDtype
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


training_root = './ACCO_DATASET/training'
X = np.empty(shape=[0, 7])
y = np.empty(shape=[0, 1])
parser = SongParser()

filelist = os.listdir(training_root)
#print(filelist)
for file in filelist:
        print(file)
        melody, acco = parser.parser_midi_training(os.path.join(training_root, file))
        #melody2 = parser.remove_header(melody)
        #melody.show('text')
        acco = parser.remove_header(acco)
        #acco.show('text')
        X_one, y_one = parser.parseSong(melody, acco)
        X, y = parser.training_join(X, X_one, y, y_one)

print(X.shape)
print(y.shape)
#print(X)
#print(y)
#print(X)
#print(y)
#model = linear_model.LogisticRegression()
model = randomForstModel()
training_data = np.hstack((X, y))
df = pd.DataFrame(training_data)
df.columns = ['head', 'tail', 'chord_inside', 'beat', 'longest', 'fre', 'first', 'chord']
#df.to_csv('traing_data.csv')
cols = ['head', 'tail', 'chord_inside', 'beat', 'longest', 'fre', 'first']
for col in cols:
        df[col] = df[col].astype(int)
        df[col] = df[col].astype(str)
#df['chord_inside'] = df['chord_inside'].astype(CategoricalDtype(categories=[0, 1, 2, 3, 4, 5, 6]))
#df['beat'] = df['beat'].astype(CategoricalDtype(categories=[0, 1, 2, 3, 4, 5, 6]))
#df['longest'] = df['longest'].astype(CategoricalDtype(categories=[0, 1, 2, 3, 4, 5, 6]))
#df['fre'] = df['fre'].astype(CategoricalDtype(categories=[0, 1, 2, 3, 4, 5, 6]))
#df['first'] = df['first'].astype(CategoricalDtype(categories=[0, 1, 2, 3, 4, 5, 6]))
#print(df.head())
train_x = pd.get_dummies(df[cols])
#print(train_x.head())
#print(train_x.shape)
label = pd.DataFrame(y)
label.columns = ['chord']
label['chord'] = label['chord'].astype(int)
#print(label)
final = pd.concat([train_x, label], axis=1)
Y = final['chord'].values
XX = final.drop('chord', axis=1).values
loss = model.train(XX, y)
#print(loss)
#print(model.coef_)
#print(final.head())
#corr = final.corr()
#df2 = pd.DataFrame(df.corr())
#print(model.score(XX, y))
#print(model.feature_importances_ )



file = './ACCO_DATASET/predict/xingkong.mid'
melody_pre = parser.parser_midi_predict(file)
#melody_pre.show()
melody_pre.show('text')

X_pre = parser.parseSong_predict(melody_pre)

#print(X_pre)
#y_pre = model.predict(X_pre)
#print(len(y_pre))
acco = parser.unparse_strumChord(y_pre)
_C_key = key.Key('C')
_44_timeSignature = meter.TimeSignature('4/4')
_55_metronomeMark =  tempo.MetronomeMark(number=55.0)
guitar = instrument.Guitar()
acco.insert(0.0, guitar)
acco.insert(_C_key)
acco.insert(_44_timeSignature)
acco.insert(_55_metronomeMark)

mf = midi.translate.streamToMidiFile(melody_pre)
mf.open("second_test.midi", 'wb')
mf.write('MusicXML')
# print("Your generated music is saved in output/my_music.midi")
mf.close()

df = pd.DataFrame(X_pre)
df.columns = ['head', 'tail', 'chord_inside', 'beat', 'longest', 'fre', 'first']
df.to_csv('xingkong.csv')
'''

