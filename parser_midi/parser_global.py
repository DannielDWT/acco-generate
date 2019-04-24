#!/usr/bin/env python
# encoding: utf-8
'''
@author: Danniel
@license: (C) Copyright
@contact: 1085837135@qq.com
@software: PyCharm
@file: parser_global.py
@time: 2019-04-03 20:21
@desc:
解析音乐所用到的一些全局变量
包括全局性表等
'''

from parser_midi.parser_music import *
from parser_midi.parser_midi import *
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest

def load_acco_dict(acco_grammars, base):
    '''
    :param acco_grammars:
    list类型，伴奏轨的一个长字符串
    :return:
    伴奏轨的对应索引表以及伴奏的元素集合
    '''
    acco_corpus = [x for sublist in acco_grammars for x in sublist.split(' ')]
    acco_values = set(acco_corpus)
    acco_val_indices =  dict((v, i + base) for i, v in enumerate(acco_values))
    acco_indices_val = dict((i + base, v) for i, v in enumerate(acco_values))
    print(acco_indices_val)
    return acco_corpus, acco_values, acco_val_indices, acco_indices_val

def load_melody_dict(melody_grammars, base):
    '''
    :param melody_grammars:
    list类型,主旋律轨的一个长字符串
    :return:
    主旋律轨的对应索引表以及主旋律的元素集合
    '''
    melody_corpus = [x for sublist in melody_grammars for x in sublist.split(' ')]
    melody_values = set(melody_corpus)
    melody_val_indices = dict((v, i + base) for i, v in enumerate(melody_values))
    melody_indices_val = dict((i + base, v) for i, v in enumerate(melody_values))
    return melody_corpus, melody_values, melody_val_indices, melody_indices_val

#----------------------------SECOND VERSION FUNCTIONS----------------------------------#

def load_acco_dict_improved(acco_grammars, base):
    '''
    :param acco_grammars:
    list类型，伴奏轨的一个长字符串
    :return:
    伴奏轨的对应索引表以及伴奏的元素集合
    '''
    acco_values = set(acco_grammars)
    acco_val_indices =  dict((v, i + base) for i, v in enumerate(acco_values))
    acco_indices_val = dict((i + base, v) for i, v in enumerate(acco_values))
    return acco_grammars, acco_values, acco_val_indices, acco_indices_val

def load_melody_dict_improved(melody_grammars):
    '''
    :param melody_grammars:
    list类型,主旋律轨的一个长字符串
    :return:
    主旋律轨的对应索引表以及主旋律的元素集合
    '''
    melody_values = set(melody_grammars)
    melody_val_indices = dict((v, i + base) for i, v in enumerate(melody_values))
    melody_indices_val = dict((i + base, v) for i, v in enumerate(melody_values))
    return melody_grammars, melody_values, melody_val_indices, melody_indices_val


