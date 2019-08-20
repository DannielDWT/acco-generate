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