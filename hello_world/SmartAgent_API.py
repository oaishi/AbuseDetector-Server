# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
from keras.layers import Dense,Input,LSTM,Bidirectional,Activation,Conv1D,GRU
from keras.callbacks import Callback
from keras.layers import Dropout,Embedding,GlobalMaxPooling1D, MaxPooling1D, Add, Flatten
from keras.preprocessing import text, sequence
from keras.layers import GlobalAveragePooling1D, GlobalMaxPooling1D, concatenate, SpatialDropout1D
from keras import initializers, regularizers, constraints, optimizers, layers, callbacks
from keras.callbacks import EarlyStopping,ModelCheckpoint
from keras.models import Model
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
#print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


import pickle
max_features=100000
maxlen=150
embed_size=300
char_max_len = 400
char_vocab_len = 256

tok_word_path = r'./hello_world/tokenizer_word.pickle'
tok_char_path = r'./hello_world/tokenizer_char.pickle'
filepath = r"./hello_world/weights_base.best.cnn_word_cnn_char.hdf5"

print('Loading token dictionary...')
with open(tok_word_path, 'rb') as handle:
    tok_word = pickle.load(handle)

with open(tok_char_path, 'rb') as handle:
    tok_char = pickle.load(handle)

print('Token dictionary loaded.')

word_index = tok_word.word_index

char_index = tok_char.word_index
#https://minimaxir.com/2017/04/char-embeddings/
#print(char_index)
char_embed_size = 16


def custom_sigmoid(x):
    y = (1 + (x / (6 + abs(x))))*0.5
    return y


channel_map = {}


def get_model():
    # model:
    sequence_input = Input(shape=(maxlen,))
    x = Embedding(max_features, embed_size, trainable=True)(sequence_input)
    x = SpatialDropout1D(0.2)(x)
    x = Bidirectional(LSTM(128, return_sequences=True, dropout=0.1, recurrent_dropout=0.1))(x)
    w_conv1 = Conv1D(32, kernel_size=1, padding="same", kernel_initializer="glorot_uniform")(x)
    w_conv2 = Conv1D(32, kernel_size=2, padding="same", kernel_initializer="glorot_uniform")(x)
    w_conv3 = Conv1D(32, kernel_size=3, padding="same", kernel_initializer="glorot_uniform")(x)
    w_conv4 = Conv1D(32, kernel_size=4, padding="same", kernel_initializer="glorot_uniform")(x)
    w_conv5 = Conv1D(32, kernel_size=5, padding="same", kernel_initializer="glorot_uniform")(x)
    w_conv = concatenate([w_conv1, w_conv2, w_conv3, w_conv4, w_conv5])
    w_avg_pool = GlobalAveragePooling1D()(w_conv)
    w_max_pool = GlobalMaxPooling1D()(w_conv)

    char_input_init = Input(shape=(char_max_len,))
    char_input = Embedding(len(char_index) + 1, char_embed_size, trainable=True)(char_input_init)
    char_input = SpatialDropout1D(0.2)(char_input)
    # char_input = Bidirectional(LSTM(128, return_sequences=True,dropout=0.1,recurrent_dropout=0.1))(char_input)
    # do characters have long term dependencies?????
    c_conv1 = Conv1D(32, kernel_size=3, padding="same", kernel_initializer="glorot_uniform")(char_input)
    c_conv2 = Conv1D(32, kernel_size=4, padding="same", kernel_initializer="glorot_uniform")(char_input)
    c_conv3 = Conv1D(32, kernel_size=5, padding="same", kernel_initializer="glorot_uniform")(char_input)
    c_conv4 = Conv1D(32, kernel_size=6, padding="same", kernel_initializer="glorot_uniform")(char_input)
    c_conv5 = Conv1D(32, kernel_size=7, padding="same", kernel_initializer="glorot_uniform")(char_input)
    c_conv = concatenate([c_conv1, c_conv2, c_conv3, c_conv4, c_conv5])
    c_avg_pool = GlobalAveragePooling1D()(c_conv)
    c_max_pool = GlobalMaxPooling1D()(c_conv)

    x = concatenate([w_avg_pool, w_max_pool, c_avg_pool, c_max_pool])

    # x = Dense(128, activation='relu')(x)
    # x = Dropout(0.1)(x)
    preds = Dense(6, activation="sigmoid")(x)

    model = Model(inputs=[sequence_input, char_input_init], outputs=preds)
    model.compile(loss='binary_crossentropy', optimizer=Adam(lr=1e-3), metrics=['accuracy'])
    #model.summary()

    return model

def load_model(filepath = filepath):
    print('building model...')
    model=get_model()
    print('model built.')
    print('loading model...')
    model.load_weights(filepath)
    print('model loaded.')
    return model


def single_sentence_tokenizer(x, tok_word=tok_word, tok_char=tok_char):
    #print('given sentence:', x)
    X_test_word = tok_word.texts_to_sequences(np.asarray([x]))
    #print('word tokens:', X_test_word)
    #print('word tokens length:', X_test_word[0].__len__())
    X_test_word = sequence.pad_sequences(X_test_word, maxlen=maxlen)

    X_test_char = tok_char.texts_to_sequences(np.asarray([x]))
    #print('char tokens:', X_test_char)
    #print('char tokens length:', X_test_char[0].__len__())
    X_test_char = sequence.pad_sequences(X_test_char, maxlen=400)

    return [X_test_word, X_test_char]


#testSentence = single_sentence_tokenizer(x='hello world! its been a longe time')

abuseDimensions = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

def predict_single_sentence(model, _sentence_):
    testSentenceTokens = single_sentence_tokenizer(x=_sentence_)
    testPrediction = model.predict(testSentenceTokens)
    # print()
    # detectionMap = {}
    # for i in range(6):
    #     detectionMap[abuseDimensions[i]] = testPrediction[0][i]
    #     # print(abuseDimensions[i], ':', testPrediction[0][i] * 100.0, '%')

    return testPrediction




import gc
gc.collect()


