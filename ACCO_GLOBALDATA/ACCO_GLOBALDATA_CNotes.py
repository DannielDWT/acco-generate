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
'''

from music21 import *

class CNotes:
    notes_num = 7
    notes_num_weight = 14
    quarter_weight = 5
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

    CNotes_To_Enum_weight = {'C':[0, 1, 2, 3],
                             'D':[4, 5, 6, 7],
                             'E':[0, 8, 9, 10],
                             'F':[1, 4, 11, 12],
                             'G':[2, 5, 8, 13],
                             'A':[3, 6, 9, 11],
                             'B':[7, 10, 12, 13]}

