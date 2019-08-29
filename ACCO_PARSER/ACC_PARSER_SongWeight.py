#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACC_PARSER_SongWeight.py
@time: 2019-08-24 9:58
@desc:
'''

from music21 import *
import numpy as np
import random
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_CNotes import CNotes
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_Chord import CChord


class SongParser_weight:

    def __init__(self):
        pass

    def parse_training(self, melody, acco):
        '''
        :param melody: 由midi文件解析出的主旋律音轨
        :param acco:  由midi文件解析出的和弦音轨
        :return: 一首歌曲组成的训练样本X与y
        该函数用于解析midi的音轨获得训练样本数据，训练样本的特征结构如上注释
        通过将音轨按小节分组，并统计小节中的各个二音符组合出现的次数, 每次出现在相应组合加上时值和权重乘积，空音符不考虑，进而组成样本数据X
        通过将和弦分组，每一小节中的和弦即为对应的输出。
        （目前存在的问题包括是否要考虑进常用的和弦变化规律以及是否考虑头部尾部C大调的特殊编配原则）
        组合格式如下：
        13, 14, 15, 16, 24, 25, 26, 27, 35, 36, 37, 46, 47, 57
        '''
        X = []
        y = []
        melody_Tuples = [(int(n.offset / 4), n) for n in melody]
        melody_m = 0
        for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
            temp = np.zeros((1, CNotes.notes_num_weight)).tolist()
            sum = 0.0
            for n in group:
                print(n[1].pitch)
                if ((isinstance(n[1], note.Rest)) or (n[1].pitch not in CNotes.CNotes_To_Enum_weight.keys())):
                    continue
                for col in CNotes.CNotes_To_Enum_weight[n[1].pitch]:
                    temp[col] += n[1].quarterLength * CNotes.quarter_weight
                    sum += temp[col]
            #归一化，避免含音符较多的小节获得较大的优势
            temp = [w / sum for w in temp]
            X.append(temp)
            melody_m += 1

        acco_measures = OrderedDict()
        offsetTuples_acco = [(int(n.offset / 4), ch) for ch in acco]
        acco_m = 0
        for key_x, group in groupby(offsetTuples_acco, lambda x: x[0]):
            #if (group.length == 0):
            if (group[0][1] not in CChord.CChord_To_Enum):
                group[0][1] = CChord.Enum_To_CChord[random.randint(0, 6)]
            y.append(CChord.CChord_To_Enum[group[0][1]])
            #acco_measures[acco_m] = [n[1] for n in group]
            acco_m += 1
        return np.mat(X), np.mat(y).transpose()
    def parse_predict(self, melody):
        '''
        :param melody: 预测样本的主旋律
        :return: 返回该首歌解析获得的预测样本
        解析用于预测的主旋律音轨，解析方法与上述一致
        '''
        X = []
        y = []
        melody_Tuples = [(int(n.offset / 4), n) for n in melody]
        melody_m = 0
        for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
            temp = np.zeros((1, CNotes.notes_num)).tolist()
            sum = 0.0
            for n in group:
                print(n[1].pitch)
                if ((isinstance(n[1], note.Rest)) or (n[1].pitch not in CNotes.CNotes_To_Enum_weight.keys())):
                    continue
                for col in CNotes.CNotes_To_Enum_weight[n[1].pitch]:
                    temp[col] += n[1].quarterLength * CNotes.quarter_weight
                    sum += temp[col]
            #归一化，避免含音符较多的小节获得较大的优势
            temp = [w / sum for w in temp]
            X.append(temp)
            melody_m += 1
        return np.mat(X)
    def unparse(self, y):
        '''
        :param y: 预测获得的m * 1维矩阵
        :return: 未加头部的伴奏音轨
        '''
        acco = stream.Stream()
        offset = 0.0
        for value in y:
            acco.insert(offset, CChord.Enum_To_CChord(value))
            offset += 4.0
        return acco

    def parse_brokenChord_training(self, melody, acco):
        '''
        :param melody: 由midi文件解析出的主旋律音轨,经header处理后
        :param acco:  由midi文件解析出的和弦音轨，经header处理后
        :return: 一首歌曲组成的训练样本X与y
        该函数用于解析midi的音轨获得训练样本数据，训练样本的特征结构如上注释
        通过将音轨按小节分组，并统计小节中的各个二音符组合出现的次数, 每次出现在相应组合加上时值和权重乘积，空音符不考虑，进而组成样本数据X
        通过将和弦分组，每一小节中的和弦即为对应的输出。
        （目前存在的问题包括是否要考虑进常用的和弦变化规律以及是否考虑头部尾部C大调的特殊编配原则）
        组合格式如下：
        13, 14, 15, 16, 24, 25, 26, 27, 35, 36, 37, 46, 47, 57

        2019-08-29 将索引方式改成字符串，并且对于没有音符对应的和弦进行抛弃，对于不具有和弦的小节样本进行抛弃 by danniel
        '''
        X = []
        y = []
        melody_Tuples = [(int(n.offset / 4), n) for n in melody]
        melody_m = 0
        for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
            temp = np.zeros((1, CNotes.notes_num_weight)).flatten().tolist()
            #print(temp)
            sum = 0.0
            for n in group:
                #print(n[1].pitch)
                if ((isinstance(n[1], note.Rest)) or (n[1].name not in CNotes.CNotes_To_Enum_weight.keys())):
                    if not isinstance(n[1], note.Rest):
                        print(n[1].name)
                    continue
                for col in CNotes.CNotes_To_Enum_weight[n[1].name]:
                    temp[col] += n[1].quarterLength * CNotes.quarter_weight
                    sum += temp[col]
            #归一化，避免含音符较多的小节获得较大的优势
            temp = [w / sum for w in temp]
            X.append(temp)
            melody_m += 1

        acco_measures = OrderedDict()
        offsetTuples_acco = [(int(ch.offset / 4), ch) for ch in acco]
        acco_m = 0
        for key_x, group in groupby(offsetTuples_acco, lambda x: x[0]):
            # if (group.length == 0):
            #print('in')
            if (acco_m > melody_m):
                #print('in2')
                break
            brokenChord_str = ''
            for n in group:
                if isinstance(n[1], note.Rest):
                    temp = ''
                else:
                    temp = str(n[1].pitch) + ' '
                brokenChord_str += temp
            brokenChord_str = brokenChord_str.strip(' ')
            #print(brokenChord_str)
            if (brokenChord_str not in CChord.brokenChord_To_Enum.keys() or brokenChord_str == ''):
                X = np.delete(X, acco_m, 0)
                melody_m -= 1
                acco_m += 1
                continue
            y.append(CChord.brokenChord_To_Enum[brokenChord_str])
            acco_m += 1
        return np.mat(X), np.mat(y).transpose()
    def parse_brokenChord_predict(self, melody):
        '''
        将需要预测的样本进行解析，返回该首歌对应的测试矩阵X
        :param melody: 经过header处理的预测样本的主旋律
        :return: X, 对应的数值矩阵
        '''
        X = []
        melody_Tuples = [(int(n.offset / 4), n) for n in melody]
        melody_m = 0
        for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
            temp = np.zeros((1, CNotes.notes_num_weight)).flatten().tolist()
            #print(temp)
            sum = 0.0
            for n in group:
                #print(n[1].pitch)
                if ((isinstance(n[1], note.Rest)) or (n[1].name not in CNotes.CNotes_To_Enum_weight.keys())):
                    #if not isinstance(n[1], note.Rest):
                    #    print(n[1].name)
                    continue
                for col in CNotes.CNotes_To_Enum_weight[n[1].name]:
                    temp[col] += n[1].quarterLength * CNotes.quarter_weight
                    sum += temp[col]
            #归一化，避免含音符较多的小节获得较大的优势
            temp = [w / sum for w in temp]
            X.append(temp)
            melody_m += 1
        return X
    def unparse_brokenChord(self, y):
        '''
        解析预测结果，翻译回伴奏轨
        :param y:  模型预测的结果
        :return:  acco 伴奏轨
        '''
        acco = stream.Stream()
        offset = 0.0
        for value in y:
            brokenChord_strList = CChord.Enum_To_brokenChord[value].split(' ')
            for n_str in brokenChord_strList:
                n = note.Note(n_str)
                n.quarterLength = 0.5
                acco.insert(offset, n)
                offset += 0.5
        return acco

    def parser_header(self, melody):
        '''
        :param melody: 主旋律音轨
        :return:
        获取训练/预测样本的头部信息
        '''
        stream_key = melody.getElementsByClass(key.Key)
        if (isinstance(stream_key, stream.iterator.StreamIterator)):
            self.__stream_key = stream_key[0]
        stream_instrument = melody.getElementsByClass(instrument.Instrument)
        if (isinstance(stream_instrument, stream.iterator.StreamIterator)):
            self.__stream_instrument = stream_instrument[0]
        stream_timeSignature = melody.getElementsByClass(meter.TimeSignature)
        if (isinstance(stream_timeSignature, stream.iterator.StreamIterator)):
            self.__stream_timeSignature = stream_timeSignature[0]
        stream_metronomeMark = melody.getElementsByClass(tempo.MetronomeMark)
        if (isinstance(stream_metronomeMark, stream.iterator.StreamIterator)):
            self.__stream_metronomeMark = stream_metronomeMark[0]
    def remove_header(self, stream_raw):
        '''
        :param stream_raw: 包含头部信息的音轨
        :return: 移除不必要信息的音轨
        '''
        processed_stream = stream.Stream()
        for nr in stream_raw:
            if isinstance(nr, note.Note) or isinstance(nr, note.Rest) or isinstance(nr, chord.Chord):
                processed_stream.insert(nr.offset, nr)
        return processed_stream
    def parser_midi_training(self, filepath):
        midi_stream = converter.parse(filepath)
        return midi_stream[0], midi_stream[1]
    def parser_midi_predict(self, filepath):
        midi_stream = converter.parse(filepath)
        return midi_stream
    def training_join(self, X1, X2, y1, y2):
        '''
        :param X1: 一首歌曲组成的训练样本X1
        :param X2: 一首歌曲组成的训练样本X2
        :param y1: 与X1对应的label
        :param y2: 与x2对应的label
        :return: 合并后的训练数据和label
        '''
        X = np.concatenate([X1, X2])
        y = np.concatenate([y1, y2])
        return X, y





if __name__ == "__main__":
    pingfan = converter.parse('../ACCO_DATASET/train/houlai.mid')
    pingfan2 = converter.parse('../ACCO_DATASET/train/yueliangdaibiaowodexin.mid')
    pingfan3 = converter.parse('../ACCO_DATASET/train/qingfeideyi.mid')
    #pingfan.show("text")
    parser = SongParser_weight()
    parser.parser_header(pingfan[0])
    processed_melody = parser.remove_header(pingfan[0])
    processed_acco = parser.remove_header(pingfan[1])
    X_one, y_one = parser.parse_brokenChord_training(processed_melody, processed_acco)
    #print(X_one.shape)
    #print(y_one.shape)
    processed_acco2 = parser.remove_header(pingfan2[1])
    processed_melody2 = parser.remove_header(pingfan2[0])
    X_two, y_two = parser.parse_brokenChord_training(processed_melody2, processed_acco2)
    #print(X_two.shape)
    #print(y_two.shape)
    X, y = parser.training_join(X_one, X_two, y_one, y_two)
    processed_acco3 = parser.remove_header(pingfan3[1])
    processed_melody3 = parser.remove_header(pingfan3[0])
    X_three, y_three = parser.parse_brokenChord_training(processed_melody3, processed_acco3)
    #print(X_two.shape)
    #print(y_two.shape)
    X_2, y_2 = parser.training_join(X, X_three, y, y_three)
    print(X_2.shape)
    print(y_2.shape)
    #print(X)
    #print(y)
