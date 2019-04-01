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
测试音乐用的是提取过音轨的melody和acco
来自于张学友的每天多爱你一些midi
使用MusicScore3进行音轨分离提取
'''

from music21 import *
from parser_midi.parser_midi import parser_Midi

acco_test = converter.parse('acco_love.mid')
melody_test = converter.parse("melody_love.mid")
acco_test_processed = acco_test[0][4]
melody_test_processed = stream.Stream()
for nr in melody_test[0]:
    if isinstance(nr, note.Note) or isinstance(nr, note.Rest):
        melody_test_processed.insert(nr.offset, nr)
parser_Midi(melody_test_processed, acco_test_processed)
