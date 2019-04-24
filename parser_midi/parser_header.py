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
from parser_midi.parser_music import *

class Header(object):
    _key = key.Key('C')
    _instrument = instrument.Instrument(instrument.Piano)
    _timeSignature = meter.TimeSignature('4/4')
    _metronomeMark = tempo.MetronomeMark(number=96.0)

    def __init__(self, melody):
        '''
        考虑如果以下元素在音轨中存在多个呢？
        :param melody:
        '''
        _instrument = melody.getElementsByClass(instrument.Instrument)
        _key = melody.getElementsByClass(key.Key)
        _timeSignature = melody.getElementsByClass(meter.TimeSignature)
        _metronomeMark = melody.getElementsByClass(tempo.MetronomeMark)


if __name__ == '__main__':
    pass