#!/usr/bin/env python
# encoding: utf-8
'''
@author: 10858
@license: (C) Copyright
@contact: xxx@qq.com
@software: PyCharm
@file: main.py
@time: 2019-04-10 17:46
@desc:
'''

from keras.models import *
from keras.layers import *
from keras.initializers import glorot_uniform
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras import backend as K
from parser_midi.parser_grammar import *
from parser_midi.parser_midi import *
from parser_midi.parser_global import *
from parser_midi.parser_music import *
from music21 import *