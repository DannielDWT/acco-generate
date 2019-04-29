#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: parser_header.py
@time: 2019-04-23 17:43
@desc:
'''

from music21 import *
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest

def get_melody_header(stream_raw):
    '''
    该函数用于提取头部信息，并产生只有音符，和弦和休止符的音轨用于进一步分析
    :param stream_raw: midi文件提取出来的流
    :return: 包含所需的音符以及提取出来的头部信息
    '''
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
    '''
    该函数用于去除伴奏头部信息，并产生只有音符，和弦和休止符的音轨用于进一步分析
    :param stream_raw: midi文件提取出来的流
    :return: 处理后的音轨
    '''
    processed_stream = stream.Stream()
    for nr in stream_raw:
        if isinstance(nr, note.Note) or isinstance(nr, note.Rest) or isinstance(nr, chord.Chord):
            processed_stream.insert(nr.offset, nr)
    return processed_stream

