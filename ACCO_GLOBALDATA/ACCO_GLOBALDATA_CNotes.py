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
    quarter_weight = 10
    class CNotesEnum:
        C = 0
        D = 1
        E = 2
        F = 3
        G = 4
        A = 5
        B = 6
    CNotes_To_Enum = {note.Note('C'):CNotesEnum.C, note.Note('D'):CNotesEnum.D, note.Note('E'):CNotesEnum.E,
                      note.Note('F'):CNotesEnum.F, note.Note('G'):CNotesEnum.G, note.Note('A'):CNotesEnum.A,
                      note.Note('B'):CNotesEnum.B}
    Enum_To_CNotes = {CNotesEnum.C: note.Note('C'), CNotesEnum.D: note.Note('D'), CNotesEnum.E: note.Note('E'),
                      CNotesEnum.F: note.Note('F'), CNotesEnum.G: note.Note('G'), CNotesEnum.A: note.Note('A'),
                      CNotesEnum.B: note.Note('B')}

    CNotes_To_Enum_weight = {note.Note('C'):[0, 1, 2, 3],
                             note.Note('D'):[4, 5, 6, 7],
                             note.Note('E'):[0, 8, 9, 10],
                             note.Note('F'):[1, 4, 11, 12],
                             note.Note('G'):[2, 5, 8, 13],
                             note.Note('A'):[3, 6, 9, 11],
                             note.Note('B'):[7, 10, 12, 13]}

