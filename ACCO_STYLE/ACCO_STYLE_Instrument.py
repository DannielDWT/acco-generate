#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_STYLE_Instrument.py
@time: 2019-08-20 10:49
@desc:
'''

from music21 import *

_C_key = key.Key('C')
_44_timeSignature = meter.TimeSignature('4/4')
_100_metronomeMark =  tempo.MetronomeMark(number=100.0)

def remove_melody_header(melody):
    pass

def remove_accopaniment_header(accopaniment):
    pass

def insert_instrument_piano(acco_stream):
    '''
    给生成的伴奏音轨添加乐器和头部
    该函数添加乐器为钢琴
    :param acco_stream:
    训练生成的伴奏音轨
    :return: acco_stream
    返回处理后的音轨
    '''
    piano = instrument.Piano()
    acco_stream.insert(0.0, piano)
    acco_stream.insert(0.0, _C_key)
    acco_stream.insert(0.0, _44_timeSignature)
    acco_stream.insert(0.0, _100_metronomeMark)
    return acco_stream

def insert_instrument_guitar(acco_stream):
    '''
    给生成的伴奏音轨添加乐器和头部
    该函数添加乐器为吉他
    :param acco_stream:
    训练生成的伴奏音轨
    :return: acco_stream
    返回处理后的音轨
    '''
    guitar = instrument.Guitar()
    acco_stream.insert(0.0, guitar)
    acco_stream.insert(0.0, _C_key)
    acco_stream.insert(0.0, _44_timeSignature)
    acco_stream.insert(0.0, _100_metronomeMark)
    return acco_stream

def insert_instrument_violin(acco_stream):
    '''
    给生成的伴奏音轨添加乐器和头部
    该函数添加乐器为小提琴
    :param acco_stream:
    训练生成的伴奏音轨
    :return: acco_stream
    返回处理后的音轨
    '''
    violin = instrument.Violin()
    acco_stream.insert(0.0, violin)
    acco_stream.insert(0.0, _C_key)
    acco_stream.insert(0.0, _44_timeSignature)
    acco_stream.insert(0.0, _100_metronomeMark)
    return acco_stream

if __name__ == '__main__':
    _C_key.show("text")
    _44_timeSignature.show("text")
    _100_metronomeMark.show("text")