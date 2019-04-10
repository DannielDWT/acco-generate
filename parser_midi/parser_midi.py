#!/usr/bin/env python
# encoding: utf-8
'''
@author: Danniel
@license: (C) Copyright
@contact: 1085837135@qq.com
@software: PyCharm
@file: parser_midi.py
@time: 2019-04-01 18:20
@desc:
对midi文件进行预处理
伴奏轨和主旋律轨分成各个小节并记录小节数
'''

from music21 import *
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest
from parser_midi.parser_music import parse_acco, unparse_acco

def parser_Midi(melody, accopaniment):
    '''
    :param melody: 主旋律音轨，理论上主要是Note类型，将其划为若干小节用dict存储
    :param accopaniment: 伴奏音轨，主要是chord类型，将其划为若干小节（与主旋律一样多）
    melody与accopaniment应当是总长度(即offset)相同，但并不是一对一关系，我们假定对应关系为
    melody中的音符对应的是最接近于但是不超过的伴奏轨的音符或者和弦
    :return:
    返回值为划分的小节（以及小节数目），划分的小节可供进一步处理以及小节数可以用于生成音乐的时候的时间偏移分析
    melody_measuers:OrderDict类型，主旋律的各个小节
    acco_measuers:OrderDict类型，伴奏的各个小节
    measures:小节数
    '''

    melody_measures = OrderedDict()
    offsetTuples_melody = [(int(n.offset / 4), n) for n in melody]
    measureNum_melody = 0
    for key_x, group in groupby(offsetTuples_melody, lambda x:x[0]):
        melody_measures[measureNum_melody] = [n[1] for n in group]
        measureNum_melody += 1

    acco_measures = OrderedDict()
    offsetTuples_acco = [(int(n.offset / 4), n) for n in accopaniment]
    measureNum_acco = 0
    for key_x, group in groupby(offsetTuples_acco, lambda x:x[0]):
        acco_measures[measureNum_acco] = [n[1] for n in group]
        measureNum_acco += 1

    #print(melody_measures)
    #print(acco_measures)
    assert len(melody_measures) == len(acco_measures)
    measures = len(melody_measures)
    return melody_measures, acco_measures, measures

#----------------------------SECOND VERSION FUNCTIONS----------------------------------#

def parser_midi_improved(melody, accopaniment):
    '''
        :param melody: 主旋律音轨，理论上主要是Note类型，用dict存储
        :param accopaniment: 伴奏音轨，主要是chord类型，与主旋律一样长
        melody与accopaniment应当是总长度(即offset)相同，但并不是一对一关系，我们假定对应关系为
        melody中的音符对应的是最接近于但是不超过的伴奏轨的音符或者和弦
        :return:
        返回值为划分的小节（以及小节数目），划分的小节可供进一步处理以及小节数可以用于生成音乐的时候的时间偏移分析
        melody_measuers:OrderDict类型，主旋律音符串
        acco_measuers:OrderDict类型，伴奏的音符串
        '''
    melody_measures = OrderedDict()
    measureNum_melody = 0
    for n in melody:
        melody_measures[measureNum_melody] = n
        measureNum_melody += 1

    acco_measures = OrderedDict()
    measureNum_acco = 0
    for n in accopaniment:
        acco_measures[measureNum_acco] = n
        measureNum_acco += 1

    #print(melody_measures)
    #print(acco_measures)
    return melody_measures, acco_measures
