import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np

stemmer=PorterStemmer()
def tokenize(sen):
    return nltk.word_tokenize(sen)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenize_sen,all_words):
    tokenize_sen=[stem(w) for w in tokenize_sen]
    bag=np.zeros(len(all_words),dtype=np.float32)
    for idx,w in enumerate(all_words):
        if w in tokenize_sen:
            bag[idx]=1
    return bag
 