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
from parser_midi.parser_music import *
from parser_midi.parser_global import *
from parser_midi.parser_grammar import *

acco_test = converter.parse('acco_love.mid')
melody_test = converter.parse("melody_love.mid")
acco_test_processed = acco_test[0][4]
melody_test_processed = stream.Stream()
for nr in melody_test[0]:
    if isinstance(nr, note.Note) or isinstance(nr, note.Rest):
        melody_test_processed.insert(nr.offset, nr)
#acco_test_processed.show("text")
#melody_measures, acco_measures, measures = parser_Midi(melody_test_processed, acco_test_processed)
melody_measures, acco_measures = parser_midi_improved(melody_test_processed, acco_test_processed)
#print(acco_measures[2].offset)
aaa = get_acco_grammars_improved(acco_measures)
bbb = get_melody_grammars_improved(melody_measures)
#get_melody_musical_data_improved(bbb)
#get_acco_musical_data_improved(aaa)
'''
aaa = get_melody_grammars(melody_measures)
bbb = get_acco_grammars(acco_measures)
'''
melody_corpus, melody_values, melody_val_indices, melody_indices_val = load_melody_dict_improved(bbb)
acco_corpus, acco_values, acco_val_indices, acco_indices_val = load_acco_dict_improved(aaa)

X, Y, n_MELODY_INDICES, N_ACCO_VALUES = parse_data(melody_corpus, acco_corpus, melody_val_indices, acco_val_indices)
y = Y[:, 1, :]
y = np.squeeze(y)
indices_y =np.argmax(y, axis=-1)
unparse_data(melody_corpus, indices_y, melody_indices_val, acco_indices_val)

