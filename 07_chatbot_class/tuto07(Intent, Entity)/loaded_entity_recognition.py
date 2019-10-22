# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 03:07:18 2019

@author: Junho
"""

import tensorflow as tf
from konlpy.tag import Okt
import ner
keras = tf.keras
t = Okt()

ner_parser = ner.Parser(t.morphs)
ner_parser.load_models()

def entity_recognition(sentence):
    return ner_parser.predict(sentence)


if __name__ == '__main__':    
    print(entity_recognition('내일 부산 날씨는?'))