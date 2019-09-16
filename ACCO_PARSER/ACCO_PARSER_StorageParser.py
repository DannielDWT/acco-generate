#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_PARSER_StorageParser.py
@time: 2019-08-20 10:39
@desc:
'''

'''
from parser_midi.parser_music import *
from parser_midi.parser_midi import *
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest

def load_acco_dict(acco_grammars, base):
    acco_corpus = [x for sublist in acco_grammars for x in sublist.split(' ')]
    acco_values = set(acco_corpus)
    acco_val_indices =  dict((v, i + base) for i, v in enumerate(acco_values))
    acco_indices_val = dict((i + base, v) for i, v in enumerate(acco_values))
    print(acco_indices_val)
    return acco_corpus, acco_values, acco_val_indices, acco_indices_val

def load_melody_dict(melody_grammars, base):
    melody_corpus = [x for sublist in melody_grammars for x in sublist.split(' ')]
    melody_values = set(melody_corpus)
    melody_val_indices = dict((v, i + base) for i, v in enumerate(melody_values))
    melody_indices_val = dict((i + base, v) for i, v in enumerate(melody_values))
    return melody_corpus, melody_values, melody_val_indices, melody_indices_val

#----------------------------SECOND VERSION FUNCTIONS----------------------------------#

def load_acco_dict_improved(acco_grammars, base):
    acco_values = set(acco_grammars)
    acco_val_indices =  dict((v, i + base) for i, v in enumerate(acco_values))
    acco_indices_val = dict((i + base, v) for i, v in enumerate(acco_values))
    return acco_grammars, acco_values, acco_val_indices, acco_indices_val

def load_melody_dict_improved(melody_grammars):
    melody_values = set(melody_grammars)
    melody_val_indices = dict((v, i + base) for i, v in enumerate(melody_values))
    melody_indices_val = dict((i + base, v) for i, v in enumerate(melody_values))
    return melody_grammars, melody_values, melody_val_indices, melody_indices_val

'''

'''
import tensorflow as tf
import keras.backend as K
from keras.layers import RepeatVector
import sys
from music21 import *
import numpy as np

def parse_data(melody_corpus, acco_corpus, melody_val_indices,
                        acco_val_indices, Tx = 50, m = 60):
    #print(melody_corpus)
    #print(len(melody_corpus))
    print(len(melody_val_indices))
    print(len(set(melody_corpus)))
    N_acco_values = len(acco_val_indices)
    N_melody_values = len(melody_val_indices)
    np.random.seed()
    X = np.zeros((m, Tx, N_melody_values), dtype=np.bool)
    Y = np.zeros((m, Tx, N_acco_values), dtype=np.bool)
    for L in range(m):
        melody_offset = 0.0
        acco_offset = 0.0
        melody_random_idx = np.random.choice(len(melody_corpus) -  Tx)
        melody_data = melody_corpus[melody_random_idx:melody_random_idx + Tx]
        for j in range(melody_random_idx):
            melody_terms = melody_corpus[j].split(',')
            offset = float(melody_terms[1])
            melody_offset += offset
        acco_idx = 0
        while acco_offset <= melody_offset:
            acco_terms = acco_corpus[acco_idx].split(',')
            offset = float(acco_terms[1])
            acco_offset += offset
            acco_idx += 1
            if (acco_idx == len(acco_corpus)):
                break
        for idx in range(Tx):
            melody_data_idx = melody_val_indices[melody_data[idx]]
            if acco_idx <= 0:
                acco_idx = 1
            acco_data_idx = acco_val_indices[acco_corpus[acco_idx - 1]]
            X[L, idx, melody_data_idx] = 1
            Y[L, idx, acco_data_idx] = 1
            melody_terms = melody_corpus[idx].split(',')
            offset = float(melody_terms[1])
            melody_offset += offset
            while acco_offset <= melody_offset:
                #print("acco: ", acco_offset)
                #print("melody: ", melody_offset)
                acco_terms = acco_corpus[acco_idx].split(',')
                offset = float(acco_terms[1])
                acco_offset += offset
                acco_idx += 1
                if (acco_idx == len(acco_corpus)):
                    break
    Y = np.swapaxes(Y, 0, 1)
    Y = Y.tolist()
    #print(X)
    #print(N_melody_values)
    #print(N_acco_values)
    return np.asarray(X), np.asarray(Y)

def unparse_data(predict_indices, acco_indices_val):
    acco_corpus = []
    acco_offset = 0.0
    #predict_indices_list = list(predict_indices)
    #print(predict_indices_list)
    #indices = list(set(predict_indices_list))
    #indices.sort(key=predict_indices_list.index)
    #print(indices)
    Y_len = len(predict_indices)
    if Y_len > 0:
        acco_corpus.append(acco_indices_val[predict_indices[0]])
    for L in range(1, Y_len):
        if predict_indices[L - 1] != predict_indices[L]:
            acco_terms = acco_indices_val[predict_indices[L]].split(',')
            acco_corpus.append(acco_indices_val[predict_indices[L]])
            acco_offset += float(acco_terms[1])

    #if len(acco_corpus) == len(set(predict_indices)):
    #    print("yes")
    print(acco_corpus)
    return acco_corpus

def parser_predict_data(melody_corpus, melody_val_indices, Tx=50):
    N_melody_values = len(set(melody_corpus))
    X = np.zeros((1, Tx, N_melody_values), dtype=np.bool)
    for idx in range(Tx):
        melody_data_idx = melody_val_indices[melody_corpus[idx]]
        X[0, idx, melody_data_idx] = 1
    return np.asarray(X)

def parser_data_multi(melody_corpus_list, acco_corpus_list, melody_val_indices, acco_val_indices, Tx=50):
    X = np.empty(shape=[0, Tx, len(melody_val_indices)])
    Y = np.empty(shape=[Tx, 0, len(acco_val_indices)])
    if len(melody_corpus_list) != acco_corpus_list:
        pass
    for i in range(len(melody_corpus_list)):
        X_temp, Y_temp = parse_data(melody_corpus_list[i], acco_corpus_list[i], melody_val_indices, acco_val_indices,
                                   Tx, m=60)
        X = np.concatenate((X, X_temp))
        Y = np.concatenate((Y, Y_temp), axis=1)
    print(X.shape)
    print(Y.shape)
    return X, Y
'''


'''
from music21 import *
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest

def get_melody_header(stream_raw):
    stream_key = stream_raw.getElementsByClass(key.Key)
    if (isinstance(stream_key, list)):
        stream_key = stream_key[0]
    stream_instrument = stream_raw.getElementsByClass(instrument.Instrument)
    if (isinstance(stream_instrument, list)):
        stream_instrument = stream_instrument[0]
    stream_timeSignature = stream_raw.getElementsByClass(meter.TimeSignature)
    if (isinstance(stream_timeSignature, list)):
        stream_timeSignature = stream_timeSignature[0]
    stream_metronomeMark = stream_raw.getElementsByClass(tempo.MetronomeMark)
    if (isinstance(stream_metronomeMark, list)):
        stream_metronomeMark = stream_metronomeMark[0]
        stream_raw.removeByNotOfClass([chord.Chord, note.Note, note.Rest])
    return stream_key, stream_instrument, stream_timeSignature, stream_metronomeMark

def remove_header(stream_raw):
    processed_stream = stream.Stream()
    for nr in stream_raw:
        if isinstance(nr, note.Note) or isinstance(nr, note.Rest) or isinstance(nr, chord.Chord):
            processed_stream.insert(nr.offset, nr)
    return processed_stream

'''


'''
from music21 import *
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest

def parser_midi(melody, accopaniment):

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
'''


'''
from music21 import *
from collections import OrderedDict, defaultdict
from itertools import groupby
import copy, random, pdb

#----------------------------FIRST VERSION FUNCTIONS----------------------------------#
def parse(measure):
    measure_copy = copy.deepcopy(measure)
    measure_copy.removeByNotOfClass([chord.Chord, note.Note, note.Rest])
    full_grammar =""
    measureStartTime = measure[0].offset - (measure[0].offset % 4)
    measureStartOffset  = measure[0].offset - measureStartTime
    for ix, nr in enumerate(measure_copy):
        elementType = ''
        info_header = ''
        info_tail = ',('
        if isinstance(nr, chord.Chord):
            elementType = 'ch'
            for n in nr.pitches:
                info_tail = info_tail + n.nameWithOctave + "-"
            info_tail = info_tail.rstrip('-')
        elif isinstance(nr, note.Note):
            elementType = 'N'
            info_tail = info_tail + nr.nameWithOctave
        elif isinstance(nr, note.Rest):
            elementType = 'R'
        if (ix == (len(measure)-1)):
            diff = measureStartTime + 4.0 - nr.offset
        else:
            diff = measure[ix + 1].offset - nr.offset
        info_header = "%s,%.3f" % (elementType, diff)
        info_tail = info_tail + ")"
        grammar_term = info_header + info_tail
        full_grammar += (grammar_term + " ")
    return full_grammar.rstrip()

def unparse(grammar):
    acco_measure = stream.Voice()
    currOffset = 0.0
    for ix, grammar_element in enumerate(grammar.split(' ')):
        terms = grammar_element.split(',')
        element_type = terms[0]
        if element_type == 'ch':
            chord_str = terms[2][1:-1]
            chords = chord_str.split('-')
            ch = chord.Chord(chords)
            ch.quarterLength = float(terms[1])
            acco_measure.insert(currOffset, ch)
        elif element_type == 'N':
            note_str = terms[2][1:-1]
            nr = note.Note(note_str)
            nr.quarterLength = float(terms[1])
            acco_measure.insert(currOffset, nr)
        elif element_type == 'R':
            nr = note.Rest()
            nr.quarterLength = float(terms[1])
            acco_measure.insert(currOffset, nr)
        currOffset += float(terms[1])
    return acco_measure

def get_melody_grammars(melody):
    melody_grammars = []
    for ix in range(0, len(melody)):
        melody_Voice = stream.Stream()
        for m in melody[ix]:
            melody_Voice.insert(m.offset, m)
        parsed = parse(melody_Voice)
        melody_grammars.append(parsed)
    print(melody_grammars)
    return melody_grammars

def get_acco_grammars(accopaniment):
    acco_grammars = []
    for ix in range(0, len(accopaniment)):
        acco_Voice = stream.Stream()
        for m in accopaniment[ix]:
            acco_Voice.insert(m.offset, m)
        parsed = parse(acco_Voice)
        acco_grammars.append(parsed)
    #print(acco_grammars)
    return acco_grammars

def get_melody_musical_data(melody_grammars):
    curr_offset = 0.0
    melody_stream = stream.Stream()
    for ix in range(0, len(melody_grammars)):
        melody_measure = unparse(melody_grammars[ix])
        for m in melody_measure:
            melody_stream.insert(curr_offset + m.offset, m)
        curr_offset += 4.0
    melody_stream.show("text")
    return melody_stream

def get_acco_musical_data(acco_grammars):
    curr_offset = 0.0
    acco_stream = stream.Stream()
    for ix in range(0, len(acco_grammars)):
        acco_measure = unparse(acco_grammars[ix])
        for m in acco_measure:
            acco_stream.insert(curr_offset + m.offset, m)
        curr_offset += 4.0
    acco_stream.show("text")
    return acco_stream

#----------------------------SECOND VERSION FUNCTIONS----------------------------------#
def parse_improved(nr, offset):
    full_grammar =""
    elementType = ''
    info_tail = ',('
    if isinstance(nr, chord.Chord):
        elementType = 'ch'
        for n in nr.pitches:
            info_tail = info_tail + n.nameWithOctave + "-"
        info_tail = info_tail.rstrip('-')
    elif isinstance(nr, note.Note):
        elementType = 'N'
        info_tail = info_tail + nr.nameWithOctave
    elif isinstance(nr, note.Rest):
        elementType = 'R'
    info_header = "%s,%.3f" % (elementType, offset)
    info_tail = info_tail + ")"
    grammar_term = info_header + info_tail
    full_grammar += grammar_term
    return full_grammar

def get_acco_grammars_improved(accopaniment):
    acco_grammars = []
    for ix in range(0, len(accopaniment)):
        nr = accopaniment[ix]
        if ix == len(accopaniment) - 1:
            offset = nr.quarterLength
        else:
            offset = accopaniment[ix + 1].offset - nr.offset
        parsed = parse_improved(nr, offset)
        acco_grammars.append(parsed)
    #print(acco_grammars)
    #print(len(acco_grammars))
    return acco_grammars

def get_melody_grammars_improved(melody):
    melody_grammars = []
    for ix in range(0, len(melody)):
        nr = melody[ix]
        if ix == len(melody) - 1:
            offset = nr.quarterLength
        else:
            offset = melody[ix + 1].offset - nr.offset
        parsed = parse_improved(nr, offset)
        melody_grammars.append(parsed)
    #print(melody_grammars)
    return melody_grammars

def get_melody_musical_data_improved(melody_grammars):
    curr_offset = 0.0
    melody_stream = stream.Stream()
    for ix in range(0, len(melody_grammars)):
        melody_measure, offset = unparse_improved(melody_grammars[ix])
        melody_stream.insert(curr_offset, melody_measure)
        curr_offset += offset
    melody_stream.show("text")
    return melody_stream

def get_acco_musical_data_improved(acco_grammars):
    curr_offset = 0.0
    acco_stream = stream.Stream()
    for ix in range(0, len(acco_grammars)):
        acco_measure, offset = unparse_improved(acco_grammars[ix])
        acco_stream.insert(curr_offset, acco_measure)
        curr_offset += offset
    acco_stream.show("text")
    return acco_stream

def unparse_improved(acco_grammar):
    terms = acco_grammar.split(',')
    offset = float(terms[1])
    element_type = terms[0]
    if element_type == 'ch':
        chord_str = terms[2][1:-1]
        chords = chord_str.split('-')
        nr = chord.Chord(chords)
        nr.quarterLength = offset
        #print(nr.quarterLength)
        return nr, offset
    elif element_type == 'N':
        note_str = terms[2][1:-1]
        nr = note.Note(note_str)
        nr.quarterLength = offset
        #print(nr.quarterLength)
        return note.Note(note_str), offset
    elif element_type == 'R':
        nr = note.Rest()
        nr.quarterLength = offset
        #print(nr.quarterLength)
        return nr, offset

#----------------------------THIRD VERSION FUNCTIONS----------------------------------#
#
# def parse_third(measure):
#     
#     对音轨进行转换的第三种方法，不在字符串中包含偏移量
#     将音符时长交给节拍进行推断
#     :param measure:
#     音轨(一小节),类型为stream.Voice
#     :return:
#     返回字符串，格式为type,(notes)
#     
#     measure_copy = copy.deepcopy(measure)
#     measure_copy.removeByNotOfClass([chord.Chord, note.Note, note.Rest])
#     full_grammar =""
#     measureStartTime = measure[0].offset - (measure[0].offset % 4)
#     measureStartOffset  = measure[0].offset - measureStartTime
#     for ix, nr in enumerate(measure_copy):
#         elementType = ''
#         info_tail = ',('
#         if isinstance(nr, chord.Chord):
#             elementType = 'ch'
#             for n in nr.pitches:
#                 info_tail = info_tail + n.nameWithOctave + "-"
#             info_tail = info_tail.rstrip('-')
#         elif isinstance(nr, note.Note):
#             elementType = 'N'
#             info_tail = info_tail + nr.nameWithOctave
#         elif isinstance(nr, note.Rest):
#             elementType = 'R'
#         info_header = "%s" % (elementType)
#         info_tail = info_tail + ")"
#         grammar_term = info_header + info_tail
#         full_grammar += (grammar_term + " ")
#     return full_grammar.rstrip()
#
# def unparse_acco_third(acco_grammar):
#     acco_measure = stream.Voice()
#     currOffset = 0.0
#     for ix, grammar_element in enumerate(acco_grammar.split(' ')):
#         terms = grammar_element.split(',')
#         element_type = terms[0]
#         if element_type == 'ch':
#             chord_str = terms[1][1:-1]
#             chords = chord_str.split('-')
#             ch = chord.Chord(chords)
#             ch.quarterLength = 4.0
#             acco_measure.insert(currOffset, ch)
#         elif element_type == 'N':
#             note_str = terms[1][1:-1]
#             nr = note.Note(note_str)
#             nr.quarterLength = 4.0
#             acco_measure.insert(currOffset, nr)
#         elif element_type == 'R':
#             nr = note.Rest()
#             nr.quarterLength = 4.0
#             acco_measure.insert(currOffset, nr)
#         currOffset += 4.0
#     return acco_measure
#
# def get_melody_grammars(melody):

#     melody_grammars = []
#     for ix in range(0, len(melody)):
#         melody_Voice = stream.Stream()
#         for m in melody[ix]:
#             melody_Voice.insert(m.offset, m)
#         parsed = parse(melody_Voice)
#         melody_grammars.append(parsed)
#     print(melody_grammars)
#     return melody_grammars
#
# def get_acco_grammars(accopaniment):

#     acco_grammars = []
#     for ix in range(0, len(accopaniment)):
#         acco_Voice = stream.Stream()
#         for m in accopaniment[ix]:
#             acco_Voice.insert(m.offset, m)
#         parsed = parse(acco_Voice)
#         acco_grammars.append(parsed)
#     #print(acco_grammars)
#     return acco_grammars
#
# def get_melody_musical_data(melody_grammars):

#     curr_offset = 0.0
#     melody_stream = stream.Stream()
#     for ix in range(0, len(melody_grammars)):
#         melody_measure = unparse(melody_grammars[ix])
#         for m in melody_measure:
#             melody_stream.insert(curr_offset + m.offset, m)
#         curr_offset += 4.0
#     melody_stream.show("text")
#     return melody_stream
#
# def get_acco_musical_data(acco_grammars):
#
#     curr_offset = 0.0
#     acco_stream = stream.Stream()
#     for ix in range(0, len(acco_grammars)):
#         acco_measure = unparse(acco_grammars[ix])
#         for m in acco_measure:
#             acco_stream.insert(curr_offset + m.offset, m)
#         curr_offset += 4.0
#     acco_stream.show("text")
#     return acco_stream
'''

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
    #melody_indices = dict(list(melody_indices_table.items()) + list(melody_val_indices.items()))
    #acco_indices = dict(list(acco_indices_table.items()) + list(acco_val_indices.items()))
    #indices_melody = dict(list(indices_melody_table.items()) + list(melody_indices_val.items()))
    #indices_acco = dict(list(indices_acco_table.items()) + list(acco_indices_val.items()))
    melody_indices = {**melody_indices_table, **melody_val_indices}
    acco_indices = {**acco_indices_table, **acco_val_indices}
    indices_melody = {**indices_melody_table, **melody_indices_val}
    indices_acco = {**indices_acco_table, **acco_indices_val}
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

'''

'''
from music21 import *

def get_full_stream(melody, accopaniment):
    melody_part = stream.Part()
    accopaniment_part = stream.Part()
    out_stream = stream.Score()
    melody_part.insert(0.0, melody)
    accopaniment_part.insert(0.0, accopaniment)
    out_stream.insert(0.0, melody_part)
    out_stream.insert(0.0, accopaniment_part)
    return out_stream
'''

# !/usr/bin/env python
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

        :param melody: 由midi文件解析出的主旋律音轨
        :param acco:  由midi文件解析出的和弦音轨
        :return: 一首歌曲组成的训练样本X与y
        该函数用于解析midi的音轨获得训练样本数据，训练样本的特征结构如上注释
        通过将音轨按小节分组，并统计小节中的各个二音符组合出现的次数, 每次出现在相应组合加上时值和权重乘积，空音符不考虑，进而组成样本数据X
        通过将和弦分组，每一小节中的和弦即为对应的输出。
        （目前存在的问题包括是否要考虑进常用的和弦变化规律以及是否考虑头部尾部C大调的特殊编配原则）
        组合格式如下：
        13, 14, 15, 16, 24, 25, 26, 27, 35, 36, 37, 46, 47, 57

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

        :param melody: 预测样本的主旋律
        :return: 返回该首歌解析获得的预测样本
        解析用于预测的主旋律音轨，解析方法与上述一致

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

        :param y: 预测获得的m * 1维矩阵
        :return: 未加头部的伴奏音轨

        acco = stream.Stream()
        offset = 0.0
        for value in y:
            acco.insert(offset, CChord.Enum_To_CChord(value))
            offset += 4.0
        return acco

    def parse_brokenChord_training(self, melody, acco):

        :param melody: 由midi文件解析出的主旋律音轨,经header处理后
        :param acco:  由midi文件解析出的和弦音轨，经header处理后
        :return: 一首歌曲组成的训练样本X与y
        该函数用于解析midi的音轨获得训练样本数据，训练样本的特征结构如上注释
        通过将音轨按小节分组，并统计小节中的各个二音符组合出现的次数, 每次出现在相应组合加上时值和权重乘积，空音符不考虑，进而组成样本数据X
        通过将和弦分组，每一小节中的和弦即为对应的输出。
        （目前存在的问题包括是否要考虑进常用的和弦变化规律以及是否考虑头部尾部C大调的特殊编配原则）
        组合格式如下：
        ##13, 14, 15, 16, 24, 25, 26, 27, 35, 36, 37, 46, 47, 57
        ##13， 24， 37， 46， 57， 36
        135, 246, 357, 461, 572, 613

        2019-08-29 将索引方式改成字符串，并且对于没有音符对应的和弦进行抛弃，对于不具有和弦的小节样本进行抛弃 by danniel
        2019-09-03 因为相关性过高根据相关性矩阵原有特征被删减如上

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

        将需要预测的样本进行解析，返回该首歌对应的测试矩阵X
        :param melody: 经过header处理的预测样本的主旋律
        :return: X, 对应的数值矩阵

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

        解析预测结果，翻译回伴奏轨
        :param y:  模型预测的结果
        :return:  acco 伴奏轨

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

        :param melody: 主旋律音轨
        :return:
        获取训练/预测样本的头部信息

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

        :param stream_raw: 包含头部信息的音轨
        :return: 移除不必要信息的音轨

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

        :param X1: 一首歌曲组成的训练样本X1
        :param X2: 一首歌曲组成的训练样本X2
        :param y1: 与X1对应的label
        :param y2: 与x2对应的label
        :return: 合并后的训练数据和label

        X = np.concatenate([X1, X2])
        y = np.concatenate([y1, y2])
        return X, y





if __name__ == "__main__":
    pingfan = converter.parse('../ACCO_DATASET/train/houlai.mid')
    pingfan2 = converter.parse('../ACCO_DATASET/train/yueliangdaibiaowodexin.mid')
    pingfan3 = converter.parse('../ACCO_DATASET/train/qingfeideyi.mid')
    pingfan4 = converter.parse('../ACCO_DATASET/train/xiaoxingyun.mid')
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
    #pingfan4.show('text')
    processed_acco4 = parser.remove_header(pingfan4[1])
    processed_melody4 = parser.remove_header(pingfan4[0])
    X_four, y_four = parser.parse_brokenChord_training(processed_melody4, processed_acco4)
    print(X_four[7])
'''
'''
def parse_str(self, melody, acco):

    :param melody: 由midi文件解析出的主旋律音轨
    :param acco: 由midi文件解析出的和弦音轨
    :return: 一首歌组成的待处理文本样本X_str, 与标记y
    该函数将音轨转化为标记y（数值数据)/类别， 而X_str则是相应的每小节对应的字符串，
    保留文本数据之后可以应用于文本分类的特征提取算法

    X = []
    y = []
    melody_Tuples = [(int(n.offset / 4), n) for n in melody]
    melody_m = 0
    for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
        temp = ''
        for n in group:
            print(n[1].pitch)
            if (isinstance(n[1], note.Rest) or n[1].pitch not in CNotes.CNotes_To_Enum):
                continue
            temp = temp + " " + n[1].pitch
        temp.strip()
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


def parse_brokenChord_training(self, melody, acco):

    :param melody: 由midi文件解析出的主旋律音轨
    :param acco:  由midi文件解析出的和弦音轨
    :return: 一首歌曲组成的训练样本X与y
    该函数用于解析midi的音轨获得训练样本数据，训练样本的特征结构如上注释
    通过将音轨按小节分组，并统计小节中的各个音符出现的次数，空音符不考虑，进而组成样本数据X
    通过将和弦分组，每一小节中的和弦即为对应的输出。
    （目前存在的问题包括是否要考虑进常用的和弦变化规律以及是否考虑头部尾部C大调的特殊编配原则）

    X = []
    y = []
    melody_Tuples = [(int(n.offset / 4), n) for n in melody]
    melody_m = 0
    for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
        temp = np.zeros((1, CNotes.notes_num)).flatten().tolist()
        sum = 0.0
        for n in group:
            #print(n[1].pitch)
            if (isinstance(n[1], note.Rest) or n[1].name not in CNotes.CNotes_To_Enum.keys()):
                continue
            temp[CNotes.CNotes_To_Enum[n[1].name]] += n[1].quarterLength * CNotes.quarter_weight
            sum += temp[CNotes.CNotes_To_Enum[n[1].name]]
        #归一化，避免含音符较多的小节获得较大的优势
        temp = [fre / sum for fre in temp]
        X.append(temp)
        melody_m += 1

    acco_measures = OrderedDict()
    offsetTuples_acco = [(int(ch.offset / 4), ch) for ch in acco]
    acco_m = 0
    for key_x, group in groupby(offsetTuples_acco, lambda x: x[0]):
        # if (group.length == 0):
        # print('in')
        if (acco_m > melody_m):
            # print('in2')
            break
        brokenChord_str = ''
        for n in group:
            if isinstance(n[1], note.Rest):
                temp = ''
            else:
                temp = str(n[1].pitch) + ' '
            brokenChord_str += temp
        brokenChord_str = brokenChord_str.strip(' ')
        # print(brokenChord_str)
        if (brokenChord_str not in CChord.brokenChord_To_Enum.keys() or brokenChord_str == ''):
            X = np.delete(X, acco_m, 0)
            melody_m -= 1
            continue
        y.append(CChord.brokenChord_To_Enum[brokenChord_str])
        acco_m += 1
    return np.mat(X), np.mat(y).transpose()
'''

'''
def parse_predict(self, melody):

    :param melody: 预测样本的主旋律
    :return: 返回该首歌解析获得的预测样本
    解析用于预测的主旋律音轨，解析方法与上述一致

    X = []
    melody_Tuples = [(int(n.offset / 4), n) for n in melody]
    melody_m = 0
    for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
        temp = np.zeros((1, CNotes.notes_num)).tolist()
        for n in group:
            print(n[1].pitch)
            if (isinstance(n[1], note.Rest) or n[1].pitch not in CNotes.CNotes_To_Enum):
                continue
            temp[CNotes.CNotes_To_Enum[n[1]]] += 1
        X.append(temp)
        melody_m += 1
    return np.mat(X)
'''

'''
    def parse_brokenChord_training(self, melody, acco):

        :param melody: 由midi文件解析出的主旋律音轨
        :param acco:  由midi文件解析出的和弦音轨
        :return: 一首歌曲组成的训练样本X与y
        该函数用于解析midi的音轨获得训练样本数据，训练样本的特征结构如上注释
        通过将音轨按小节分组，并统计小节中的各个音符出现的次数，空音符不考虑，进而组成样本数据X
        通过将和弦分组，每一小节中的和弦即为对应的输出。
        （目前存在的问题包括是否要考虑进常用的和弦变化规律以及是否考虑头部尾部C大调的特殊编配原则）

        X = []
        y = []
        melody_Tuples = [(int(n.offset / 4), n) for n in melody]
        melody_m = 0
        for key_x, group in groupby(melody_Tuples, lambda x: x[0]):
            temp = np.zeros((1, CNotes.notes_num_weight)).flatten().tolist()
            sum = 0.0
            for n in group:
                #print(n[1].pitch)
                if (isinstance(n[1], note.Rest) or (n[1].name not in CNotes.CNotes_To_Enum.keys())):
                    continue
                temp[CNotes.CNotes_To_Enum[n[1].name]] += n[1].quarterLength * CNotes.quarter_weight
                sum += temp[CNotes.CNotes_To_Enum[n[1].name]]
            # 归一化，避免含音符较多的小节获得较大的优势
            temp = [fre / sum for fre in temp]
            X.append(temp)
            melody_m += 1

        acco_measures = OrderedDict()
        offsetTuples_acco = [(int(ch.offset / 4), ch) for ch in acco]
        acco_m = 0
        for key_x, group in groupby(offsetTuples_acco, lambda x: x[0]):
            # if (group.length == 0):
            # print('in')
            if (acco_m > melody_m):
                # print('in2')
                break
            brokenChord_str = ''
            for n in group:
                if isinstance(n[1], note.Rest):
                    temp = ''
                else:
                    temp = str(n[1].pitch) + ' '
                brokenChord_str += temp
            brokenChord_str = brokenChord_str.strip(' ')
            # print(brokenChord_str)
            if (brokenChord_str not in CChord.brokenChord_To_Enum.keys() or brokenChord_str == ''):
                X = np.delete(X, acco_m, 0)
                melody_m -= 1
                acco_m += 1
                continue
            y.append(CChord.brokenChord_To_Enum[brokenChord_str])
            acco_m += 1
        return np.mat(X), np.mat(y).transpose()
'''