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
    # 將data中所有文章的i字Counter都集合起來
    contentGramFreqs= collections.Counter()
    for content in data:
        gramFreqs= collections.Counter(ngrams([*content], i))
        contentGramFreqs+= gramFreqs
    
    # 從有了lastGramFreqs的第2個迴圈開始，都要逐詞進行比對
    if lastGramFreqs:
        for gramFreq in contentGramFreqs:
            # 將出現次數少於(文章數*0.5)次的字詞排除掉
            if contentGramFreqs[gramFreq] >= len(data)/2:
                # ex: 所有文章中，'屈臣氏'出現的次數/'屈臣'出現的次數(*暫時稱為馬可夫機率)。這個數值越接近1，代表越有可能是一個不可分割的詞
                hMarkov[gramFreq]= contentGramFreqs[gramFreq]/ lastGramFreqs[gramFreq[:-1]]
                
                # ex: 如果'屈臣'的馬可夫機率與'屈臣氏'很接近，那就把'屈臣'pop掉，保留'屈臣氏'就好
                if gramFreq[:-1] in hMarkov.keys() and hMarkov[gramFreq]/ hMarkov[gramFreq[:-1]] >=0.8:
                    hMarkov.pop(gramFreq[:-1])
                
    # 將這一個迴圈所做的(i字)counter，留到下一個迴圈，以供下一個迴圈(i+1字)的比對
    lastGramFreqs= contentGramFreqs

# 按照馬可夫機率排序
hMarkov= dict(sorted(hMarkov.items(), key=lambda x:x[1], reverse=True))



for i,m in enumerate(hMarkov):
    if i < 100:
        print(m, hMarkov[m])

