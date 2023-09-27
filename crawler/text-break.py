# 使用python-embed版時要加這2行
import sys, os
sys.path.append(os.path.dirname(__file__))

import collections
from nltk.util import ngrams
from db import *




# 要抓取的最大字詞長度
wordMaxLen= 5
# 最低出現次數(平均每篇文章要有0.5次)
threshold= 0.5


data= getData("youtube", "SELECT videoContent FROM youtube")
data= [row[0] for row in data]


hMarkov= {}
freqs= {}
for wordNum in range(1,wordMaxLen+1):
    # 將data中所有文章的i字Counter都集合起來
    contentGramFreqs= collections.Counter()
    for content in data:
        # 把content中的每個字都拆開，變成一個list後，再丟給ngrams
        contentGramFreqs+= collections.Counter(ngrams([*content], wordNum))
    
    # 從有了lastGramFreqs的第2個迴圈開始，都要逐詞進行比對
    if freqs:
        for gramFreq in contentGramFreqs:
            # 將出現次數少於(文章數*0.5)次的字詞排除掉
            if contentGramFreqs[gramFreq] >= len(data)*threshold:
                # ex: 所有文章中，'屈臣氏'出現的次數/'屈臣'出現的次數(*暫時稱為馬可夫機率)。這個數值越接近1，代表越有可能是一個不可分割的詞
                # hMarkov[gramFreq]= contentGramFreqs[gramFreq]/ freqs[gramFreq[:-1]]
                # 但是像'的感覺'.'覺得比較'之類的東西，在樣本數多的時候不怎麼會出現，但是樣本數少的時候就有可能沒有被篩選掉，所以這邊是將字詞再做更多輪的比對
                # ex: '屈臣氏'出現的次數要除以'屈臣'的次數，以及'屈'的次數，再將兩者做平均 (/'屈臣'後的數值高，/'屈'後的數值也同樣高，故不會被篩選掉)
                # ex: '的感覺'出現的次數要除以'的感'的次數，以及'覺'的次數，再將兩者做平均 (/'的感'後的數值高，/'的'後的數值超低，故會被篩選掉)
                # ex: '但我覺得'出現的次數要除以'但我覺'的次數(超高) & '但我'的次數(高) & '但'(超低)的次數，再將三者做平均
                hMarkovPossible= []
                for splitNum in range(1, wordNum):
                    hMarkovPossible.append(contentGramFreqs[gramFreq]/ freqs[gramFreq[:-splitNum]])
                hMarkov[gramFreq]= sum(hMarkovPossible)/len(hMarkovPossible)
                
    # 將這一個迴圈所做的(i字)counter，留到下一個迴圈，以供下一個迴圈(i+1字)的比對
    freqs= {**freqs, **contentGramFreqs}

# 按照馬可夫機率排序
hMarkov= dict(sorted(hMarkov.items(), key=lambda x:x[1], reverse=True))



for i,m in enumerate(hMarkov):
    if i < 100:
        print(m, "\t馬可夫機率:", hMarkov[m], "\t出現次數", freqs[m])

