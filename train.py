import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader
import numpy as np
import json
from nltk_utils import tokenize,stem,bag_of_words
from model import NeuralNet

with open('intents.json','r') as f:
    intents=json.load(f)

all_words=[]
tags=[]
xy=[]

for intent in intents['intents']:
    tag=intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        pattern=tokenize(pattern)
        all_words.extend(pattern)
        xy.append((pattern,tag))

punct=['?',',','.']
all_words=[stem(w) for w in all_words if w not in punct]
all_words=sorted(set(all_words))
tags=sorted(set(tags))

X_train=[]
Y_train=[]

for (pattern_tokenized,tag) in xy:
    bag=bag_of_words(pattern_tokenized,all_words)
    X_train.append(bag)
    label=tags.index(tag)
    Y_train.append(label)

X_train=np.array(X_train)
Y_train=np.array(Y_train)

class chatdataset(Dataset):
    def __init__(self):
        self.n_samples=len(X_train)
        self.x_data=X_train
        self.y_data=Y_train
    def __getitem__(self,index):
        return self.x_data[index],self.y_data[index]
    def __len__(self):
        return self.n_samples
#Hyperparameters
num_epocks=1000
learning_rate=0.001
batch_size=8
input_size=len(X_train[0])
output_size=len(tags)
hidden_size=8


dataset=chatdataset()
train_loader=DataLoader(dataset=dataset,batch_size=batch_size,num_workers=0,shuffle=True)

model=NeuralNet(input_size,hidden_size,output_size)
loss=nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(model.parameters(),lr=learning_rate)

for epocs in range(num_epocks):
    for (bag,label) in train_loader:
        label=label.to(dtype=torch.long)
        predicted_label=model(bag)
        l=loss(predicted_label,label)
        l.backward()
        optimizer.step()
        optimizer.zero_grad()

FILE='data.pth'
data={
    'input_size':input_size,
    'output_size':output_size,
    'hidden_size':hidden_size,
    'all_words':all_words,
    'tags':tags,
    'model_state':model.state_dict()
}
torch.save(data,FILE)
print("Data Dumped Sucessfully.")