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
from music_style.instrument import *
from music21 import *
from model import *

acco_test = converter.parse('acco_love.mid')
melody_test = converter.parse("melody_love.mid")
acco1, acco2 = acco_test.getElementsByClass(stream.Part)
acco_test_processed, acco3 = acco1.getElementsByClass(stream.Voice)
melody_test_processed = stream.Stream()
for nr in melody_test[0]:
    if isinstance(nr, note.Note) or isinstance(nr, note.Rest):
        melody_test_processed.insert(nr.offset, nr)
melody_measures, acco_measures = parser_midi_improved(melody_test_processed, acco_test_processed)
aaa = get_acco_grammars_improved(acco_measures)
bbb = get_melody_grammars_improved(melody_measures)
melody_corpus, melody_values, melody_val_indices, melody_indices_val = load_melody_dict_improved(bbb)
acco_corpus, acco_values, acco_val_indices, acco_indices_val = load_acco_dict_improved(aaa)

X, Y, N_melody_values, N_acco_values = parse_data(melody_corpus, acco_corpus, melody_val_indices, acco_val_indices)

n_a = 64
reshapor = Reshape((1, N_melody_values))
LSTM_cell = LSTM(n_a, return_state=True)
densor = Dense(N_acco_values, activation='softmax')

model = tranning_model(50, n_a, N_melody_values, N_acco_values, reshapor, LSTM_cell, densor)
opt = Adam(lr=0.01, beta_1=0.9, beta_2=0.999, decay=0.01)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
m = 60
a0 = np.zeros((m, n_a))
c0 = np.zeros((m, n_a))
model.fit([X, a0, c0], list(Y), epochs=100)

inference_model = predict_model(reshapor, LSTM_cell, densor, len(melody_corpus), N_melody_values, N_acco_values, n_a=64)
x_initializer = parser_predict_data(melody_corpus, melody_val_indices)
a_initializer = np.zeros((1, n_a))
c_initializer = np.zeros((1, n_a))
x_initializer = np.reshape(x_initializer, (1, len(melody_corpus), N_melody_values))
#print(x_initializer.shape)
pred = inference_model.predict([x_initializer, a_initializer, c_initializer])
indices = np.argmax(pred, axis = -1)
indices = indices.squeeze()
indices = indices.tolist()
#print(indices)
acco_corpus = unparse_data(indices, acco_indices_val)
acco_stream = get_acco_musical_data_improved(acco_corpus)
acco_stream.show("text")

out_stream1 = stream.Part()
out_stream = stream.Stream()
out_stream1.insert(0.0, acco_stream)
out_stream1.insert(0.0, acco3)
out_stream.insert(out_stream1)
out_stream.insert(acco2)
out_stream = insert_instrument_piano(out_stream)

mf = midi.translate.streamToMidiFile(out_stream)
mf.open("my_music3.midi", 'wb')
mf.write()
#print("Your generated music is saved in output/my_music.midi")
mf.close()