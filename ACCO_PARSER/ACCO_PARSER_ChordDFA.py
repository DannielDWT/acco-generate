#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: ACCO_PARSER_ChordDFA.py
@time: 2019-08-24 11:52
@desc:
'''
'''
from music21 import *
import numpy as np
import random
from collections import defaultdict, OrderedDict
from itertools import groupby, zip_longest
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_CNotes import CNotes
from ACCO_GLOBALDATA.ACCO_GLOBALDATA_Chord import CChord
from enum import IntEnum, unique

class DFA_state(IntEnum):
    
    该枚举类用于表示有限状态机里面的各个状态
    其中命名规则为：
    C1_1,第一个1表示常见套路第几，第二个表示在套路中的位置
    C2o3_2中间有o表示两个套路共同使用一个状态
    C1_5_1中间下划线表示连续5个套路共用该状态
    
    READY = -1
    C1_5_1 = 0
    F1_2 = 1
    Am2o3_2 = 2
    Dm4_2 = 3
    G5_2 = 4
    G1o4_3 = 5
    F2_3 = 6
    Dm3_3 = 7
    Am5_3 = 8
    C1_5_4o5o8 = 9
    G2o3_4 = 10
    F5_4 = 11
    Em5_5 = 12
    Dm5_6 = 13
    G5_7 = 14

class ChordDFA:
    
    该类用于转换当前状态，同时返回相应的各个列应该增加的权重
    从而使得预测时某些列权重更大，更倾向于预测为某一类和弦
    该类接受预测时的当前预测值作为输入，并返回一个字典，索引为列，值为权重
    权重由 总权重 与位置因子构成
    

    def __init__(self):
        self.__state = DFA_state.READY
        self.__totalWeight = 0.2
        self.__FIRST = 4
        self.__SECOND = 5
        self.__THIRD = 5
        self.__FOURTH = 4
        self.__FIFTH = 8

    def transition(self, predict_y):
        if (self.__state == DFA_state.READY):
            if (predict_y == CChord.CChord_To_Enum[CChord.C]):
                self.__state = DFA_state.C1_5_1
            else:
                self.__state = DFA_state.READY
            return self.__READY()

        elif (self.__state == DFA_state.C1_5_1):
            if (predict_y == CChord.CChord_To_Enum[CChord.F]):
                self.__state = DFA_state.F1_2
            elif (predict_y == CChord.CChord_To_Enum[CChord.Am]):
                self.__state = DFA_state.Am2o3_2
            elif (predict_y == CChord.CChord_To_Enum[CChord.Dm]):
                self.__state = DFA_state.Dm2_3
            elif (predict_y == CChord.CChord_To_Enum[CChord.G]):
                self.__state = DFA_state.G5_2
            else:
                self.__state = DFA_state.READY
            return self.__C1_5_1()

        elif (self.__state == DFA_state.F1_2):
            if (predict_y == CChord.CChord_To_Enum[CChord.G]):
                self.__state = DFA_state.G1o4_3
            else:
                self.__state = DFA_state.READY
            return self.__F1_2()

        elif (self.__state == DFA_state.Am2o3_2):
            if (predict_y == CChord.CChord_To_Enum[CChord.F]):
                self.__state = DFA_state.F2_3
            elif (predict_y == CChord.CChord_To_Enum[CChord.Dm]):
                self.__state = DFA_state.Dm3_3
            else:
                self.__state = DFA_state.READY
            return self.__Am2o3_2()

        elif (self.__state == DFA_state.Dm4_2):
            if (predict_y == CChord.CChord_To_Enum[CChord.G]):
                self.__state = DFA_state.G1o4_3
            else:
                self.__state = DFA_state.READY
            return self.__Dm4_2()

        elif (self.__state == DFA_state.G5_2):
            if (predict_y == CChord.CChord_To_Enum[CChord.Am]):
                self.__state = DFA_state.Am5_3
            else:
                self.__state = DFA_state.READY
            return self.__G5_2()

        elif (self.__state == DFA_state.G1o4_3):
            if (predict_y == CChord.CChord_To_Enum[CChord.C]):
                self.__state = DFA_state.C1_5_4o5o8
            else:
                self.__state = DFA_state.READY
            return self.__G1o4_3()

        elif (self.__state == DFA_state.F2_3):
            if (predict_y == CChord.CChord_To_Enum[CChord.G]):
                self.__state = DFA_state.G2o3_4
            else:
                self.__state = DFA_state.READY
            return self.__F2_3()

        elif (self.__state == DFA_state.Dm2_3):
            if (predict_y == CChord.CChord_To_Enum[CChord.G]):
                self.__state = DFA_state.G2o3_4
            else:
                self.__state = DFA_state.READY
            return self.__Dm2_3()

        elif (self.__state == DFA_state.Am5_3):
            if (predict_y == CChord.CChord_To_Enum[CChord.F]):
                self.__state = DFA_state.F5_4
            else:
                self.__state = DFA_state.READY
            return self.__Am5_3()

        elif (self.__state == DFA_state.C1_5_4o5o8):
            self.__state = DFA_state.READY
            return self.__C1_5_4o5o8()
        elif (self.__state == DFA_state.G2o3_4):
            if (predict_y == CChord.CChord_To_Enum[CChord.C]):
                self.__state = DFA_state.C1_5_4o5o8
            else:
                self.__state = DFA_state.READY
            return self.__G2o3_4()
        elif (self.__state == DFA_state.F5_4):
            if (predict_y == CChord.CChord_To_Enum[CChord.Em]):
                self.__state = DFA_state.Em5_5
            else:
                self.__state = DFA_state.READY
            return self.__F5_4()
        elif (self.__state == DFA_state.Em5_5):
            if (predict_y == CChord.CChord_To_Enum[CChord.Dm]):
                self.__state = DFA_state.Dm5_6
            else:
                self.__state = DFA_state.READY
            return self.__Em5_5()
        elif (self.__state == DFA_state.Dm5_6):
            if (predict_y == CChord.CChord_To_Enum[CChord.G]):
                self.__state = DFA_state.G5_7
            else:
                self.__state = DFA_state.READY
            return self.__Dm5_6()
        elif (self.__state == DFA_state.G5_7):
            if (predict_y == CChord.CChord_To_Enum[CChord.C]):
                self.__state = DFA_state.C1_5_4o5o8
            else:
                self.__state = DFA_state.READY
            return self.__G5_7()

    def __READY(self):
        return {}
    def __C1_5_1(self):
        result = {}
        chords = [CChord.Am, CChord.F, CChord.Dm, CChord.G]
        for chord in chords:
            cols = CChord.Enum_To_Column_weight[chord]
            for col in cols:
                if col not in result.keys():
                    result[col] = 0.025
                else:
                    result[col] += 0.025 #可以考虑再除以一个可能的出口数，即下一个和弦可能数目，因为害怕和弦交叠导致某些列重复增加
                    #第一个位置由于后续各种可能长度没法统一一个权重值
        return result
    def __F1_2(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.G]
        for col in cols:
            result[col] = self.__totalWeight / self.__FIRST * 2
        return result
    def __Am2o3_2(self):
        result = {}
        chords = [CChord.F, CChord.Dm]
        for chord in chords:
            cols = CChord.Enum_To_Column_weight[chord]
            for col in cols:
                if col not in result.keys():
                    result[col] = self.__totalWeight / self.__SECOND * 2
                else:
                    result[col] += self.__totalWeight / self.__SECOND * 2  #同样考虑排除重叠影响
        return result
    def __Dm4_2(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.G]
        for col in cols:
            result[col] = self.__totalWeight / self.__THIRD * 2
        return result
    def __G5_2(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.Am]
        for col in cols:
            result[col] = self.__totalWeight / self.__FIFTH * 2
        return result
    def __G1o4_3(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.C]
        for col in cols:
            result[col] = self.__totalWeight / self.__FIRST * 3
        return result
    def __F2_3(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.G]
        for col in cols:
            result[col] = self.__totalWeight / self.__SECOND * 3
        return result
    def __Dm2_3(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.G]
        for col in cols:
            result[col] = self.__totalWeight / self.__THIRD * 3
        return result
    def __Am5_3(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.F]
        for col in cols:
            result[col] = self.__totalWeight / self.__FIFTH * 3
        return result
    def __C1_5_4o5o8(self):
        return {}
    def __G2o3_4(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.C]
        for col in cols:
            result[col] = self.__totalWeight / self.__SECOND * 4
        return result
    def __F5_4(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.Em]
        for col in cols:
            result[col] = self.__totalWeight / self.__FIFTH * 4
        return result
    def __Em5_5(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.Dm]
        for col in cols:
            result[col] = self.__totalWeight / self.__FIFTH * 5
        return result
    def __Dm5_6(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.G]
        for col in cols:
            result[col] = self.__totalWeight / self.__FIFTH * 6
        return result
    def __G5_7(self):
        result = {}
        cols = CChord.Enum_To_Column_weight[CChord.C]
        for col in cols:
            result[col] = self.__totalWeight / self.__FIFTH * 7
        return result
'''