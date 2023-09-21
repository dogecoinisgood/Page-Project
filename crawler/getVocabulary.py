# 使用python-embed版時要加這2行
import sys, os, time, re
sys.path.append(os.path.dirname(__file__))



from db import *
import nltk, re, string, collections
from nltk.util import ngrams

data= getData("youtube", "SELECT videoContent FROM youtube")

BigramFreqs= []
for row in data:
    Bigrams = ngrams(row[0], 2)
    BigramFreq= collections.Counter(Bigrams)
    BigramFreqs.append(Bigrams)

print(BigramFreqs[0])
sum(BigramFreqs)



