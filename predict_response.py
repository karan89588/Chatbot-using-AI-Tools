import json
import torch
import torch.nn as nn
from model import NeuralNet
from nltk_utils import tokenize,stem,bag_of_words
import random

with open('intents.json','r') as f:
    intents=json.load(f)

FILE='data.pth'
data=torch.load(FILE)

input_size=data['input_size']
output_size=data['output_size']
hidden_size=data['hidden_size']
all_words=data['all_words']
tags=data['tags']
model_state=data['model_state']

model=NeuralNet(input_size,hidden_size,output_size)
model.load_state_dict(model_state)
model.eval()



def get_response(msg):
    msg=tokenize(msg)
    bag=bag_of_words(msg,all_words)
    bag=torch.from_numpy(bag)
    bag=bag.reshape(1,bag.shape[0])
    output=model(bag)
    _,predicted=torch.max(output,dim=1)
    tag=tags[predicted.item()]
    probabilities=torch.softmax(output,dim=1)
    probability=probabilities[0][predicted.item()]
    if(probability>0.75):
        for intent in intents['intents']:
            if tag==intent['tag']:
                return random.choice(intent['responses'])
    else:
        return "I can't got you"

if __name__=='__main__':
    print(get_response('hi'))