# 使用python-embed版時要加這2行
import sys, os, time, re
sys.path.append(os.path.dirname(__file__))

import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from db import *



newArtical= '''
在彩妝世界中，粉底液是一個關鍵的步驟，它能為你的妝容提供均勻、霧面的妝效，同時遮瑕不完美，成為一個完美的妝前打底。我們很高興向大家推薦一個全新系列的粉底液，它將讓你的彩妝達到新的高度，提亮你的眼妝，讓你的妝容更加出色。
霧面妝效：這個系列的粉底液以其霧面的妝效而著稱，無論你是在日常生活中使用還是在特殊場合上妝，都能為你帶來自然、無瑕的妝容。它的質地輕盈，易於推開，不會讓你的皮膚感到沉重，而且能夠持久保持霧面妝效。
提亮眼妝：這個粉底液特別適合用來提亮眼妝。它的特殊配方可以讓眼皮顯得更加明亮，同時能夠修飾眼袋和黑眼圈，讓你的眼妝更加閃亮夺目。無論你是在打造日常的日間妝還是參加晚宴，這款粉底液都能為你的眼妝增色不少。
遮瑕效果：除了提亮眼妝，這個粉底液還具有出色的遮瑕效果。它可以遮住瑕疵，如痘痘、疤痕和紅血絲，讓你的肌膚看起來更加光滑、均勻。無論你的肌膚類型如何，這款粉底液都能為你提供所需的遮瑕效果。
適合眼妝：這個系列的粉底液不僅適合用來提亮眼妝，還可以作為眼妝的理想打底產品。它的質地柔軟，容易推開，可以幫助眼影更好地附著在眼皮上，提供更持久的眼妝效果。此外，它還可以幫助睫毛膏更好地附著在睫毛上，讓你的睫毛更長、更濃密。
包裝精美：這個系列的粉底液不僅在妝效上令人滿意，在包裝上也讓人愛不釋手。它採用了時尚的包裝設計，外觀優雅大方，適合放在化妝包中攜帶。無論你是在家中上妝還是外出旅行，都可以輕鬆攜帶這款粉底液。
使用刷子：為了獲得最佳的妝效，我們建議使用專業的妝刷來塗抹這款粉底液。刷子可以幫助你更均勻地塗抹粉底液，讓妝容更加完美。
總之，這個全新系列的粉底液將成為你化妝包中的必備品。它不僅具有出色的霧面妝效和遮瑕效果，還能提亮眼妝，適合眼妝使用，並且擁有精美的包裝。無論你是化妝初學者還是彩妝達人，都會愛上這款粉底液。立即嘗試，讓你的彩妝妝效更加完美！
'''



model_name= "distiluse-base-multilingual-cased-v2"
model_path= os.path.abspath(os.path.join(base_path, "crawler/data/sentence-transformers", model_name))

if os.path.exists(model_path):
    model = SentenceTransformer(model_path)
else:
    model = SentenceTransformer(model_name)
    model.save(model_path)

# 中文測試
# wordpairs = [['老師', '教師', '泰國'], 
#              ['商品', '貨物', '跑步'],
#              ['商品', '商品', '產品'],
#             ]
# for wordpair in wordpairs:
#     embeddings = model.encode(wordpair)
#     print(wordpair[0], 'vs',  wordpair[1], 'distance =', util.pytorch_cos_sim(embeddings[0], embeddings[1]))
#     print(wordpair[0], 'vs',  wordpair[2], 'distance =', util.pytorch_cos_sim(embeddings[0], embeddings[2]))
#     print(wordpair[1], 'vs',  wordpair[2], 'distance =', util.pytorch_cos_sim(embeddings[1], embeddings[2]))

data= getData("youtube", "SELECT videoContent,views,likes,dislikes FROM youtube")

data= sorted(data, key=lambda x:(x[2]-x[3])/x[1], reverse=True)


# for row in data[:50]:
#     print(row[0][:15], row[1], row[2], row[3], (row[2]-row[3])/row[1], sep='\t')


# data= [row[0] or '' for row in data][:30]
data= data[:30]
# sentence_embeddings = model.encode(data, show_progress_bar=True)

embeddings = model.encode([row[0] or '' for row in data]+[newArtical])

diss= []
for i,row in enumerate(data):
    diss.append(util.pytorch_cos_sim(embeddings[i], embeddings[-1]))
    print(i, row[0][:30], diss[-1], sep='\t')
# diss= [util.pytorch_cos_sim(embeddings[i], embeddings[-1]) for i,row in enumerate(data)]

print(sum(diss)/len(diss))
