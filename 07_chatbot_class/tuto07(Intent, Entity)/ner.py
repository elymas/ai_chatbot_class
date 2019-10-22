import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


class Parser:

    def __init__(self, tokenizer):
        # ::Hard coded char lookup ::
        self.tokenizer = tokenizer

    def load_models(self, loc=None):
        if loc == None:
            self.model = load_model("Entity/model.h5")
            # loading word2Idx
            self.word2Idx = np.load("Entity/word2Idx.npy", allow_pickle=True).item()
            # loading idx2Label
            self.idx2Label = np.load("Entity/idx2Label.npy", allow_pickle=True)
            # loading char2Idx
            self.char2Idx = np.load("Entity/char2Idx.npy", allow_pickle=True).item()
        else:
            self.model = load_model(os.path.join(loc,"model.h5"))
            # loading word2Idx
            self.word2Idx = np.load(os.path.join(loc, "Entity/word2Idx.npy"), allow_pickle=True).item()
            # loading idx2Label
            self.idx2Label = np.load(os.path.join(loc, "Entity/idx2Label.npy"), allow_pickle=True).item()
            # loading char2Idx
            self.char2Idx = np.load(os.path.join(loc, "Entity/char2Idx.npy"), allow_pickle=True).item()
    def createTensor(self,sentence, word2Idx, char2Idx):
        unknownIdx = word2Idx['_UNK_']
    
        wordIndices = []    
        charIndices = []
            
        for word, char in sentence:  
            word = str(word)
            if word in word2Idx:
                wordIdx = word2Idx[word]              
            else:
                wordIdx = unknownIdx
            charIdx = []
            for x in char:
                if x in char2Idx.keys():
                    charIdx.append(char2Idx[x])
                else:
                    charIdx.append(char2Idx['_UNK_'])   
            wordIndices.append(wordIdx)
            charIndices.append(charIdx)
            
        return [wordIndices, charIndices]

    def addCharInformation(self, sentence):
        return [[word, list(str(word))] for word in sentence]

    def padding(self,Sentence):
        Sentence[1] = pad_sequences(Sentence[1],15,padding='post')
        return Sentence

    def predict(self,Sentence):
        Sentence = words =  self.tokenizer(Sentence)
        Sentence = self.addCharInformation(Sentence)
        Sentence = self.padding(self.createTensor(Sentence,self.word2Idx,self.char2Idx))
        tokens, char = Sentence
        tokens = np.asarray([tokens])     
        char = np.asarray([char])
        pred = self.model.predict([tokens, char], verbose=False)[0]   
        pred = pred.argmax(axis=-1)
        pred = [self.idx2Label[x].strip() for x in pred]
        return list(zip(words,pred))