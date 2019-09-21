#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_GLOBALDATA_CNotes.py
@time: 2019-08-18 19:59
@desc:
存储了音符对应的枚举类型和音符表
'''

from music21 import *

class CNotes:
    notes_num = 7
    attr_num = 7
    class CNotesEnum:
        C = 0
        D = 1
        E = 2
        F = 3
        G = 4
        A = 5
        B = 6
    CNotes_To_Enum = {'C':CNotesEnum.C, 'D':CNotesEnum.D, 'E':CNotesEnum.E,
                      'F':CNotesEnum.F, 'G':CNotesEnum.G, 'A':CNotesEnum.A,
                      'B':CNotesEnum.B}
    Enum_To_CNotes = {CNotesEnum.C: 'C', CNotesEnum.D: 'D', CNotesEnum.E: 'E',
                      CNotesEnum.F: 'F', CNotesEnum.G: 'G', CNotesEnum.A: 'A',
                      CNotesEnum.B: 'B'}


