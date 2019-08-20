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
from parser_midi.parser_midi import parser_midi
from parser_midi.parser_music import *
from parser_midi.parser_global import *
from parser_midi.parser_grammar import *
from parser_midi.parser_song import *
from parser_midi.parser_header import *

acco_test = converter.parse('acco_love.mid')
melody_test = converter.parse("melody_love.mid")
test = converter.parse("./dataset/kexibushini.mid")
test2 = converter.parse("./dataset/tonghua.mid")
test2.show("text")
print(len(melody_test))
print(len(acco_test))
acco1, acco2 = acco_test.getElementsByClass(stream.Part)
acco_test_processed, acco3 = acco1.getElementsByClass(stream.Voice)
melody_test_processed = stream.Stream()
stream_key, stream_instrument, stream_timeSignature, stream_metronomeMark  = remove_header(melody_test[0])
stream_key.show("text")
for nr in melody_test[0]:
    if isinstance(nr, note.Note) or isinstance(nr, note.Rest):
        melody_test_processed.insert(nr.offset, nr)
melody_list = []
acco_list = []
melody_list.append(melody_test_processed)
acco_list.append(acco_test_processed)
melody_corpus_list, acco_corpus_list, indices_melody_table, indices_acco_table, melody_indices_table, \
acco_indices_table = parser_table(melody_list, acco_list)
parser_data_multi(melody_corpus_list, acco_corpus_list, melody_indices_table, acco_indices_table)

