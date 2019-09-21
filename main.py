#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: main.py
@time: 2019-04-10 17:46
@desc:
主执行文件
pre_file路径为要预测的主旋律文件所在的路径
training_root为训练文件文件夹
target_file为生成的含伴奏文件所在处
'''


from music21 import *
from ACCO_PARSER.ACCO_PARSER_Song import SongParser
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_CNotes import CNotes
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_Chord import CChord
from ACCO_MODEL.ACCO_MODEL_SVMModel import SVCModel
from ACCO_MODEL.ACCO_MODEL_DescionTree import DecisionTreeModel
from ACCO_MODEL.ACCO_MODEL_RandomForestModel import randomForstModel
from pandas.api.types import CategoricalDtype
from sklearn import linear_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


training_root = './ACCO_DATASET/training'
pre_file = './ACCO_DATASET/predict/tonghua.mid'
target_file = './ACCO_OUTPUT/tonghua.mid'

X = np.empty(shape=[0, 7])
y = np.empty(shape=[0, 1])
parser = SongParser()
filelist = os.listdir(training_root)
for file in filelist:
        melody, acco = parser.parser_midi_training(os.path.join(training_root, file))
        acco = parser.remove_header(acco)
        X_one, y_one = parser.parseSong(melody, acco)
        X, y = parser.training_join(X, X_one, y, y_one)

n_train = len(X)
melody_pre = parser.parser_midi_predict(pre_file)
X_pre = parser.parseSong_predict(melody_pre)
n_pre = len(X_pre)
print(X_pre.shape)


model = randomForstModel()

df_train = pd.DataFrame(X)
df_test = pd.DataFrame(X_pre)
df = pd.concat([df_train, df_test])
df.columns = ['head', 'tail', 'chord_inside', 'beat', 'longest', 'fre', 'first']
for col in df.columns:
        df[col] = df[col].astype(int)
        df[col] = df[col].astype(str)

full = pd.get_dummies(df)
train_x = full[:n_train]
pre_x = full[n_train:]
X = train_x.values
loss = model.train(X, y)

y_pre = model.predict(pre_x.values)
print(y_pre.shape)

full = stream.Part()
full.insert(0.0, melody_pre)

acco = parser.unparse_brokenChord(y_pre)
_C_key = key.Key('C')
_44_timeSignature = meter.TimeSignature('4/4')
_55_metronomeMark =  tempo.MetronomeMark(number=90)
guitar = instrument.Guitar()
acco.insert(0.0, guitar)
acco.insert(_C_key)
acco.insert(_44_timeSignature)
acco.insert(_55_metronomeMark)

full.insert(0.0, acco)

mf = midi.translate.streamToMidiFile(full)
mf.open(target_file, 'wb')
mf.write()
print("Your generated music is saved in %s" % target_file)
mf.close()