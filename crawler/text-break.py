# 使用python-embed版時要加這2行
import sys, os
sys.path.append(os.path.dirname(__file__))

import collections
from nltk.util import ngrams
from db import *




data= getData("youtube", "SELECT videoContent FROM youtube")
data= [row[0] for row in data]




hMarkov= {}
lastGramFreqs= {}
for i in range(5):
    contentGramFreqs= None
    for content in data:
        gramFreqs= collections.Counter(ngrams([*content], i))
        if contentGramFreqs:
            contentGramFreqs+= gramFreqs
        else:
            contentGramFreqs= gramFreqs
    
    if lastGramFreqs:
        for gramFreq in contentGramFreqs:
            hMarkov[gramFreq]= contentGramFreqs[gramFreq]/ lastGramFreqs[gramFreq[:-1]]
    
    lastGramFreqs= contentGramFreqs

hMarkov= dict(sorted(hMarkov.items(), key=lambda x:x[1], reverse=True))

for i,m in enumerate(hMarkov):
    if i < 10:
        print(m, hMarkov[m])
