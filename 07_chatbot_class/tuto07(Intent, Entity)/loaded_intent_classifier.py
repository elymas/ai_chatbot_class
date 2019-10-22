# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 01:48:08 2019

@author: Junho
"""

import tensorflow as tf
from konlpy.tag import Okt
from vectorizer import BaseVectorizer
import numpy as np
import pickle

MAX_LENGTH = 50

keras = tf.keras
t = Okt()
tokenizer = BaseVectorizer(t.morphs)

loaded_model = keras.models.load_model("./Intent/saved_intent_model.h5")
tokenizer.load('./Intent/input_tokenizer.vocab')
with open('./Intent/id_to_intent.pickle', 'rb') as handle:
    id_to_label = pickle.load(handle)

def question_processing(sentences):
    inputs = []
    for sentence in sentences:
        # tokenize sentence
        tokenized_sentence = tokenizer.encode_a_doc_to_list(sentence)
        # check tokenized sentence max length
        if len(tokenized_sentence) <= MAX_LENGTH:
            inputs.append(tokenized_sentence)
        else:
            print('입력이 너무 길어요.')
    # pad tokenized sentences
    padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(inputs, maxlen=MAX_LENGTH, padding='post', 
                                                                  value = tokenizer.vocabulary_['_PAD_']) # value = 0
    return padded_inputs


def intent_classifier(sentence):
    input_sentence = question_processing(sentence)
    prediction = np.argmax(loaded_model.predict(input_sentence), axis=1)
    
    return id_to_label[int(prediction)]

if __name__ == '__main__':
    print(intent_classifier(['서울 내일 날씨 어때?']))