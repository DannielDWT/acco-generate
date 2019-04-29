#!/usr/bin/env python
# encoding: utf-8
'''
@author: Danniel
@license: (C) Copyright
@contact: 1085837135@qq.com
@software: PyCharm
@file: parser_full_stream.py
@time: 2019-04-28 20:47
@desc:
包含用于将生成的伴奏和主旋律处理到一起的函数
生成各种风格的歌曲
'''

from music21 import *

def get_full_stream(melody, accopaniment):
    '''
    :param melody: 主旋律
    :param accopaniment:  伴奏
    :return:
    '''
    melody_part = stream.Part()
    accopaniment_part = stream.Part()
    out_stream = stream.Score()
    melody_part.insert(0.0, melody)
    accopaniment_part.insert(0.0, accopaniment)
    out_stream.insert(0.0, melody_part)
    out_stream.insert(0.0, accopaniment_part)
    return out_stream