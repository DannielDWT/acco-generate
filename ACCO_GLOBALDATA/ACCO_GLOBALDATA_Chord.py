#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_GLOBALDATA_Chord.py
@time: 2019-08-18 14:38
@desc:
包含相关类型的和弦生成字典（表）的全局数据文件
存储了和弦对应的枚举类型，和扫弦，分界和弦以及正常时值为4的三音同弹和弦
'''


from music21 import *


class CChord:
    class CChordEnum:
        C = 0
        DM = 1
        EM = 2
        F = 3
        G = 4
        AM = 5
        G7 = 6
        #E7 = 7

    brokenChord_To_Enum = {'C3 G3 C4 G3 E4 G3 C4 G3': CChordEnum.C,
                           'A2 A3 C4 A3 E4 A3 C4 A3': CChordEnum.AM,
                           'E3 G3 B3 G3 E4 G3 B3 G3': CChordEnum.EM,
                           'D3 A3 D4 A3 F4 A3 D4 A3': CChordEnum.DM,
                           'G2 G3 B3 G3 G4 G3 B3 G3': CChordEnum.G,
                           'F3 A3 C4 A3 F4 A3 C4 A3': CChordEnum.F}

    Enum_To_brokenChord = {CChordEnum.C: 'C3 G3 C4 G3 E4 G3 C4 G3',
                           CChordEnum.AM: 'A2 A3 C4 A3 E4 A3 C4 A3',
                           CChordEnum.EM: 'E3 G3 B3 G3 E4 G3 B3 G3',
                           CChordEnum.DM: 'D3 A3 D4 A3 F4 A3 D4 A3',
                           CChordEnum.G: 'G2 G3 B3 G3 G4 G3 B3 G3',
                           CChordEnum.F: 'F3 A3 C4 A3 F4 A3 C4 A3'}

    brokenChord_To_strumChord = {'C3 G3 C4 G3 E4 G3 C4 G3': 'E2 C3 E3 G3 C4 E4',
                                 'A2 A3 C4 A3 E4 A3 C4 A3': 'E2 A2 E3 A3 C4 E4',
                                 'E3 G3 B3 G3 E4 G3 B3 G3': 'E2 B2 E3 G3 B3 E4',
                                 'D3 A3 D4 A3 F4 A3 D4 A3': 'E2 A2 D3 A3 D4 F4',
                                 'G2 G3 B3 G3 G4 G3 B3 G3': 'G2 B2 D3 G3 B3 G4',
                                 'F3 A3 C4 A3 F4 A3 C4 A3': 'F2 C3 F3 A3 C4 F4'}

    Enum_To_strumChord = {CChordEnum.C: 'E2 C3 E3 G3 C4 E4',
                           CChordEnum.AM: 'E2 A2 E3 A3 C4 E4',
                           CChordEnum.EM: 'E2 B2 E3 G3 B3 E4',
                           CChordEnum.DM: 'E2 A2 D3 A3 D4 F4',
                           CChordEnum.G: 'G2 B2 D3 G3 B3 G4',
                           CChordEnum.F: 'F2 C3 F3 A3 C4 F4'}

    strumChord_To_Enum = {'E2 C3 E3 G3 C4 E4': CChordEnum.C,
                          'E2 A2 E3 A3 C4 E4': CChordEnum.AM,
                          'E2 B2 E3 G3 B3 E4': CChordEnum.EM,
                          'E2 A2 D3 A3 D4 F4': CChordEnum.DM,
                          'G2 B2 D3 G3 B3 G4': CChordEnum.G,
                          'F2 C3 F3 A3 C4 F4': CChordEnum.F}

    Enum_To_Chord = {CChordEnum.C: 'C4 E4 G4',
                     CChordEnum.AM: 'A3 C4 E4',
                     CChordEnum.EM: 'G3 B3 E4',
                     CChordEnum.DM: 'D3 F3 A3',
                     CChordEnum.G: 'G3 B3 D4',
                     CChordEnum.F: 'F3 A3 C4'}

    Chord_To_Enum = {'C4 E4 G4': CChordEnum.C,
                     'A3 C4 E4': CChordEnum.AM,
                     'G3 B3 E4': CChordEnum.EM,
                     'D3 F3 A3': CChordEnum.DM,
                     'G3 B3 D4': CChordEnum.G,
                     'F3 A3 C4': CChordEnum.F}



