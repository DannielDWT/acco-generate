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

#----------------------------SECOND VERSION FUNCTIONS----------------------------------#
def parse_improved(nr, offset):
    '''
    :param nr:
    音符，主要为和弦，普通音符和休止音符,类型为note, chord, rest
    :return:
    返回用字符串表示的midi音符
    字符串格式为: type,offset,time,(notes)
    '''
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
    info_header = "%s,%.3f,%.3f" % (elementType, offset, nr.quarterLength)
    info_tail = info_tail + ")"
    grammar_term = info_header + info_tail
    full_grammar += grammar_term
    return full_grammar

def get_acco_grammars_improved(accopaniment):
    '''
    :param accopaniment:
    OrderDict()类型，存储的是各个伴奏小节
    :return:
    返回所有小节对应的一个长字符串
    '''
    acco_grammars = []
    for ix in range(0, len(accopaniment)):
        nr = accopaniment[ix]
        if ix == len(accopaniment) - 1:
            offset = nr.quarterLength
        else:
            offset = accopaniment[ix + 1].offset - nr.offset
        parsed = parse_improved(nr, offset)
        acco_grammars.append(parsed)
    print(acco_grammars)
    print(len(acco_grammars))
    return acco_grammars

def get_melody_grammars_improved(melody):
    '''
    :param melody:
    OrderDict()类型，存储的是主旋律音符集合
    :return:
    返回对应的一个长字符串,list
    '''
    melody_grammars = []
    for ix in range(0, len(melody)):
        nr = melody[ix]
        if ix == len(melody) - 1:
            offset = nr.quarterLength
        else:
            offset = melody[ix + 1].offset - nr.offset
        parsed = parse_improved(nr, offset)
        melody_grammars.append(parsed)
    print(melody_grammars)
    return melody_grammars

def get_melody_musical_data_improved(melody_grammars):
    '''
    :param melody_grammars:
    一个长字符串,list类型
    :return:
    返回一个完整的主旋律音轨（不含乐器等）
    '''
    curr_offset = 0.0
    melody_stream = stream.Stream()
    for ix in range(0, len(melody_grammars)):
        melody_measure, offset = unparse_improved(melody_grammars[ix])
        melody_stream.insert(curr_offset, melody_measure)
        curr_offset += offset
    melody_stream.show("text")
    return melody_stream

def get_acco_musical_data_improved(acco_grammars):
    '''
    :param acco_grammars:
    所有小节对应的一个长字符串
    :return:
    返回一个完整的伴奏音轨（不含乐器等）
    '''
    curr_offset = 0.0
    acco_stream = stream.Stream()
    for ix in range(0, len(acco_grammars)):
        acco_measure, offset = unparse_improved(acco_grammars[ix])
        acco_stream.insert(curr_offset, acco_measure)
        curr_offset += offset
    acco_stream.show("text")
    return acco_stream

def unparse_improved(acco_grammar):
    '''
    :param acco_grammar:
    用字符串表示的伴奏音轨（单个），格式为type,time(notes)
    :return:
    返回stream.Voice类型的音轨
    '''
    terms = acco_grammar.split(',')
    offset = float(terms[1])
    element_type = terms[0]
    if element_type == 'ch':
        chord_str = terms[3][1:-1]
        chords = chord_str.split('-')
        nr = chord.Chord(chords)
        nr.quarterLength = float(terms[2])
        #print(nr.quarterLength)
        return nr, offset
    elif element_type == 'N':
        note_str = terms[3][1:-1]
        nr = note.Note(note_str)
        nr.quarterLength = float(terms[2])
        #print(nr.quarterLength)
        return note.Note(note_str), offset
    elif element_type == 'R':
        nr = note.Rest()
        nr.quarterLength = float(terms[2])
        #print(nr.quarterLength)
        return nr, offset