#!/usr/bin/env python
# encoding: utf-8
'''
@author: Danniel
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: parser_music.py
@time: 2019-03-31 16:16
@desc:
该文件包含用于将midi文件解析为字符串
以及将特定字符串解析成midi文件的函数
'''

from music21 import *
from collections import OrderedDict, defaultdict
from itertools import groupby
import copy, random, pdb


f = note.Note("C3");
e7 = chord.Chord("E4 G#4 B4 D5")
print(f.nameWithOctave)
for L in e7.pitches:
    print(L.nameWithOctave)


def parse_acco(acco):
    '''
    :param chords:
    伴奏音轨，主要为和弦
    :return:
    返回用字符串表示的midi音轨
    字符串格式为: type,time(notes)
    '''
    acco_copy = copy.deepcopy(acco)
    acco_copy.removeByNotOfClass([chord.Chord, note.Note, note.Rest])

