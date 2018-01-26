# -*- coding: utf-8 -*-

import sys
import pandas
import os
import keras
import io
import numpy as np
import random

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop

homepath=os.path.expanduser('~')

def make_vector():

    text=io.open('input text', encoding='utf-8').read().lower()
    print('corpus length:', len(text))
    chars = sorted(list(set(text)))
    print('total chars:', len(chars))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    # cut the text in semi-redundant sequences of maxlen characters
    maxlen = 40
    step = 3
    sentences = []
    next_chars = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
    print('nb sequences:', len(sentences))

    print('Vectorization...')
    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1
    # build the model: a single LSTM
    print('Build model...')
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))

    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    def sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    fw = open('output text','w')
    # train the model, output generated text after each iteration
    # 学習回数を決定
    for iteration in range(1, 60):
        print()
        print('-' * 50)
        print('Iteration', iteration)
        fw.write('Iteration'+ str(iteration)+'\n')
        model.fit(x, y,
                  batch_size=128,
                  epochs=1)

        start_index = random.randint(0, len(text) - maxlen - 1)

        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print()
            print('----- diversity:', diversity)
            fw.write('----- diversity:'+str(diversity)+'\n')

            generated = ''
            #sentence = text[start_index: start_index + maxlen]
            sentence='楽しい！美味しい！！'
            generated += sentence

            print('----- Generating with seed: "' + sentence + '"')
            fw.write('----- Generating with seed: "' + sentence + '"\n')
            sys.stdout.write(generated)
            fw.write(generated+'\n')

            for i in range(400):
                x_pred = np.zeros((1, maxlen, len(chars)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, char_indices[char]] = 1.

                preds = model.predict(x_pred, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = indices_char[next_index]

                generated += next_char
                sentence = sentence[1:] + next_char

                sys.stdout.write(next_char)
                fw.write(next_char)
                sys.stdout.flush()
            print()
            fw.write('\n')


if __name__ == '__main__':
    make_vector()
    #test()
    #adjusttext()
