#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_PARSER_Song.py
@time: 2019-08-18 20:47
@desc:
解析midi文件输出训练或预测数据
X结构如下:
    C D E F G A B
    (样本数据为其出现次数,忽略空音符，从乐理上空音符不造成影响{考虑忽略头部尾部训练样本})
y结构为:
    chord
    (数值为对应的在globaldata的数字)

2019-08-23 1. 考虑加入多个音一组的作为特征，单音的影响可能会出问题
            (考虑的解决方案之一，将所用七个音直接组成二二对(和三三对)作为特征（特征数过多，考虑直接从和弦本身组合入手））
            14个特征(两两组合)，在出现的地方相应加权重
            (解决方案之二，通过一个神经网络，两层隐层？神经网络去组织可能的组合）
           2. 考虑加入时长特征，通过引入一个时长因子来使音的时长也体现出来，否则音长但音少的音极有可能被视为不重要音
2019-09-16 1. 采用新的解析方法，特征为 歌曲头部， 歌曲尾部， 和弦内音， 强拍音， 最长音， 频次最高音， 小节第一个音
           2. 删除或将过往解析方法移到storageParser
2019-09-19 1. 加入扫弦
2019-09-21 1. 加入三音同时弹奏的和弦
'''

from music21 import *
import numpy as np
import random
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_CNotes import CNotes
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_Chord import CChord


class SongParser:

    def __init__(self):
        self.predict_remove = []
        pass

    def unparse_brokenChord(self, y):
        '''
        :param y: 预测获得的m * 1维矩阵
        :return: 未加头部的伴奏音轨
        '''
        acco = stream.Stream()
        offset = 0.0
        index = 0
        for value in y:
            if index in self.predict_remove:
                self.predict_remove.remove(index)
                index += 1
                offset += 4.0
                continue
            brokenChord_strList = CChord.Enum_To_brokenChord[value].split(' ')
            for bc in brokenChord_strList:
                print(bc)
                n = note.Note(bc)
                n.quarterLength = 0.5
                acco.insert(offset, n)
                offset += 0.5
            index += 1
        return acco
    def unparse_strumChord(self, y):
        acco = stream.Stream()
        offset = 0.0
        index = 0
        for value in y:
            if index in self.predict_remove:
                self.predict_remove.remove(index)
                index += 1
                offset += 4.0
                continue
            strumChord_str = CChord.Enum_To_strumChord[int(value)]
            ch_length = [1, 0.5, 0.25, 0.25, 1, 0.5, 0.25, 0.25]
            for length in ch_length:
                ch = chord.Chord(strumChord_str)
                ch.quarterLength = length
                acco.insert(offset, ch)
                offset += length
            index += 1
        return acco

    def unparse_Chord(self, y):
        acco = stream.Stream()
        offset = 0.0
        index = 0
        for value in y:
            if index in self.predict_remove:
                self.predict_remove.remove(index)
                index += 1
                offset += 4.0
                continue
            chord_str = CChord.Enum_To_Chord[int(value)]
            ch = chord.Chord(chord_str)
            ch.duration = duration.Duration(4.0)
            ch.quarterLength = 4.0
            acco.insert(offset, ch)
            offset += 4.0
            index += 1
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
        return midi_stream[0]
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
    def containsChord(self, notesStr):
        '''
        判断小节内是否包含某个和弦的组成音
        :param chordStr:
        :return:
        '''
        if ('C' in notesStr and 'E' in notesStr and 'G' in notesStr):
            return 1
        elif ('D' in notesStr and 'F' in notesStr and 'A' in notesStr):
            return 2
        elif ('E' in notesStr and 'G' in notesStr and 'B' in notesStr):
            return 3
        elif ('F' in notesStr and 'A' in notesStr and 'C' in notesStr):
            return 4
        elif ('G' in notesStr and 'B' in notesStr and 'D' in notesStr):
            return 5
        elif ('A' in notesStr and 'C' in notesStr and 'E' in notesStr):
            return 6
        else:
            return 0
    def parseSong(self, melody, acco):
        '''
        将歌曲解析成训练数据
        特征为： 是否是第一小节 是否是最后一节  和弦内音对应的和弦 强拍音 小节最长音 频数最大音
        :param melody:
        :param acco:
        :return: X, y
        '''
        X = []
        y = []
        melody_m = 0
        melody_Tuples = [(int(n.offset / 4), n) for n in melody]
        acco_Tuples = [(int(ch.offset / 4), ch) for ch in acco]
        head = 0
        tail = melody_Tuples[len(melody_Tuples) - 1][0]
        for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
            temp = np.zeros((1, CNotes.attr_num)).astype(np.int32).flatten().tolist()
            if key_x == head:
                temp[0] = 1
            if key_x == tail:
                temp[1] = 1
            beatStrengthNotes = {}
            longestNotes = {}
            freNotes = {}
            notesStr = ''
            first = True
            for n in group:
                if (not isinstance(n[1], note.Note)):
                    continue
                if (isinstance(n[1], note.Rest) or n[1].name not in CNotes.CNotes_To_Enum.keys()):
                    continue
                if (first):
                    temp[6] = CNotes.CNotes_To_Enum[n[1].name]
                    first = False
                if (n[1].name not in beatStrengthNotes.keys() or n[1].beatStrength > beatStrengthNotes[n[1].name]):
                    #print(n[1].name)
                    beatStrengthNotes[n[1].name] = n[1].beatStrength
                if (n[1].name not in longestNotes.keys() or n[1].quarterLength > beatStrengthNotes[n[1].name]):
                    longestNotes[n[1].name] = n[1].quarterLength
                if (n[1].name not in freNotes.keys()):
                    freNotes[n[1].name] = 1
                else:
                    freNotes[n[1].name] += 1
                notesStr += n[1].name
            temp[2] = self.containsChord(notesStr)
            temp[3] = CNotes.CNotes_To_Enum[max(beatStrengthNotes, key=beatStrengthNotes.get)]
            temp[4] = CNotes.CNotes_To_Enum[max(longestNotes, key=longestNotes.get)]
            temp[5] = CNotes.CNotes_To_Enum[max(freNotes, key=freNotes.get)]
            melody_m += 1
            X.append(temp)

        offsetTuples_acco = [(int(ch.offset / 4), ch) for ch in acco]
        acco_m = 0
        for key_x, group in groupby(offsetTuples_acco, lambda x: x[0]):
            if (acco_m > melody_m):
                break
            brokenChord_str = ''
            for n in group:
                if isinstance(n[1], note.Rest):
                    temp = ''
                else:
                    temp = str(n[1].pitch) + ' '
                brokenChord_str += temp
            brokenChord_str = brokenChord_str.strip(' ')
            if (brokenChord_str not in CChord.brokenChord_To_Enum.keys() or brokenChord_str == ''):
                X = np.delete(X, acco_m, 0)
                melody_m -= 1
                continue
            y.append(CChord.brokenChord_To_Enum[brokenChord_str])
            acco_m += 1
        return np.mat(X), np.mat(y).transpose()
    def parseSong_predict(self, melody):
        '''
        解析预测数据，单首歌曲，返回相应的训练数据X
        :param melody:
        :return:
        '''
        X = []
        melody_m = 0
        melody_Tuples = [(int(n.offset / 4), n) for n in melody]
        head = 0
        tail = melody_Tuples[len(melody_Tuples) - 1][0]
        for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
            temp = np.zeros((1, CNotes.attr_num)).astype(np.int32).flatten().tolist()
            if key_x == head:
                temp[0] = 1
            if key_x == tail:
                temp[1] = 1
            beatStrengthNotes = {}
            longestNotes = {}
            freNotes = {}
            notesStr = ''
            first = True
            for n in group:
                if (not isinstance(n[1], note.Note)):
                    continue
                if (isinstance(n[1], note.Rest) or n[1].name not in CNotes.CNotes_To_Enum.keys()):
                    continue
                if (first):
                    temp[6] = CNotes.CNotes_To_Enum[n[1].name]
                    first = False
                if (n[1].name not in beatStrengthNotes.keys() or n[1].beatStrength > beatStrengthNotes[n[1].name]):
                    #print(n[1].name)
                    beatStrengthNotes[n[1].name] = n[1].beatStrength
                if (n[1].name not in longestNotes.keys() or n[1].quarterLength > beatStrengthNotes[n[1].name]):
                    longestNotes[n[1].name] = n[1].quarterLength
                if (n[1].name not in freNotes.keys()):
                    freNotes[n[1].name] = 1
                else:
                    freNotes[n[1].name] += 1
                notesStr += n[1].name
            temp[2] = self.containsChord(notesStr)
            temp[3] = CNotes.CNotes_To_Enum[max(beatStrengthNotes, key=beatStrengthNotes.get)]
            temp[4] = CNotes.CNotes_To_Enum[max(longestNotes, key=longestNotes.get)]
            temp[5] = CNotes.CNotes_To_Enum[max(freNotes, key=freNotes.get)]
            melody_m += 1
            X.append(temp)
        return np.mat(X)



