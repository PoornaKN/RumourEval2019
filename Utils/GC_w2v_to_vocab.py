# -*- coding: utf-8 -*-
"""w2v_to_vocab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hdr9OrpwXKNjP_G-b2LGo5tVjIIyTTMQ
"""

!wget https://github.com/mmihaltz/word2vec-GoogleNews-vectors/blob/master/GoogleNews-vectors-negative300.bin.gz

import gzip

with gzip.open('GoogleNews-vectors-negative300.bin.gz.1','rb') as f:
  file_content=f.read()

open('w2v.bin','wb').write(file_content)





!wget "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"

from gensim.models.keyedvectors import KeyedVectors

# this is how you load the model
model = KeyedVectors.load_word2vec_format(r'w2v.bin', binary=True)

import pickle
with open('vocab.pkl','rb') as r:
  vocab=pickle.load(r)

print (len(vocab))

wordVec = model.vocab;
d = dict()
for word in vocab:
	if word in wordVec: 
		d[word] = model[word]
	
print(len(d))

with open('vocab2vec.pkl', 'wb') as handle:
	pickle.dump(d, handle)

with open('vocab2vec.pkl','rb') as r:
  s=pickle.load(r)

print (len(s.keys()))