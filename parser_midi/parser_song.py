#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: parser_song.py
@time: 2019-04-23 22:21
@desc:
'''

from music21 import *
from parser_midi.parser_midi import parser_midi
from parser_midi.parser_music import *
from parser_midi.parser_global import *
from parser_midi.parser_grammar import *

def parser_table_single(melody, acco, indices_melody_table, indices_acco_table, melody_indices_table, acco_indices_table):
    melody_measures, acco_measures, measures = parser_midi(melody, acco)
    acco_grammars = get_acco_grammars(acco_measures)
    melody_grammars = get_melody_grammars(melody_measures)
    melody_corpus, melody_values, melody_val_indices, melody_indices_val = load_melody_dict(melody_grammars,
                                                                                            len(melody_indices_table))
    acco_corpus, acco_values, acco_val_indices, acco_indices_val = load_acco_dict(acco_grammars, len(acco_indices_table))
    melody_indices = dict(list(melody_indices_table.items()) + list(melody_val_indices.items()))
    acco_indices = dict(list(acco_indices_table.items()) + list(acco_val_indices.items()))
    indices_melody = dict(list(indices_melody_table.items()) + list(melody_indices_val.items()))
    indices_acco = dict(list(indices_acco_table.items()) + list(acco_indices_val.items()))
    return melody_corpus, acco_corpus, indices_melody, indices_acco, melody_indices, acco_indices

def parser_table(melody_list, acco_list):
    if len(melody_list) != len(acco_list):
        pass
    indices_melody_table = dict()
    indices_acco_table = dict()
    melody_indices_table = dict()
    acco_indices_table = dict()
    melody_corpus_list = []
    acco_corpus_list = []
    for i in range(len(melody_list)):
        melody_corpus, acco_corpus, indices_melody_temp, indices_acco_temp, melody_indices_temp, acco_indices_temp = \
            parser_table_single(melody_list[i], acco_list[i], indices_melody_table, indices_acco_table, melody_indices_table,
                                acco_indices_table)
        indices_melody_table = indices_melody_temp
        indices_acco_table = indices_acco_temp
        melody_indices_table = melody_indices_temp
        acco_indices_table = acco_indices_temp
        melody_corpus_list.append(melody_corpus)
        acco_corpus_list.append(acco_corpus)
    print(indices_acco_table)
    print(acco_corpus_list)
    return melody_corpus_list, acco_corpus_list, indices_melody_table, indices_acco_table, melody_indices_table, acco_indices_table



