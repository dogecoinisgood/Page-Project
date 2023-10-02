# 使用python-embed版時要加這2行
import sys, os, time, re
sys.path.append(os.path.dirname(__file__))

import os
from sentence_transformers import SentenceTransformer, util
from db import *




if os.path.exists("data/sentence-transformers/base-v1"):
    model = SentenceTransformer('data/sentence-transformers/base-v1')
else:
    model = SentenceTransformer('paraphrase-distilroberta-base-v1')
    model.save("data/sentence-transformers/base-v1")

# # 中文測試
# wordpairs = [['老師', '教師', '泰國'], 
#              ['商品', '貨物', '跑步'],
#              ['商品', '商品', '產品']]
# for wordpair in wordpairs:
#     embeddings = model.encode(wordpair)
#     print(wordpair[0], 'vs',  wordpair[1], 'distance =', util.pytorch_cos_sim(embeddings[0], embeddings[1]))
#     print(wordpair[0], 'vs',  wordpair[2], 'distance =', util.pytorch_cos_sim(embeddings[0], embeddings[2]))
#     print(wordpair[1], 'vs',  wordpair[2], 'distance =', util.pytorch_cos_sim(embeddings[1], embeddings[2]))

data= getData("youtube", "SELECT videoContent FROM youtube")
data= [row[0] for row in data]

sentence_embeddings = model.encode(data, show_progress_bar=True)

