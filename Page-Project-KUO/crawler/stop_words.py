# ckiptagger: 中研院開發之繁體中文專用斷詞程式；功能與jieba類似

import os, re
from ckiptagger import WS, POS, NER
from db import getData
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


# ----------------------------------------------------------------------------------------------------------------------- #


corpus= getData("youtube","SELECT videoContent FROM youtube")
corpus2= getData("youtube2","SELECT videoContent FROM youtube2")

corpus= [row[0] for row in corpus][:330]  # [:N] 取用N篇文本
# corpus2= [row[0] for row in corpus][:284]  # [:N] 取用N篇文本
# corpus= [row[0] for row in corpus][:20]  # [:N] 取用N篇文本

# corpus= corpus+corpus2
# 導入CKIPtagger 斷詞模型
ws = WS('D:\desktopD\git\Page-Project-Kuo\Page-Project\Page-Project-KUO\crawler\ws_model')

# 讀取文本（corpus）
# path = r'C:\Users\User\Desktop\cosmetic_1.txt'  # 測試單一一篇文本時使用此區塊
# with open(path, 'r', encoding='utf-8') as f :
#     corpus = f.readlines()

# 文本清理，刪除 "【】"、"《》"、"「」" 等符號
collect_corpus = []
for i in corpus:
    clean_c = re.sub('[【】《》「」]', '', i)
    if len(clean_c) > 0:
        collect_corpus.append(clean_c)

# 執行斷詞
word_segment = ws(collect_corpus,
                  sentence_segmentation=True,
                  segment_delimiter_set={'?', '？', '!', '！', '。', '.', ',', '，', ';', ':', '、'})

# ----------------------------------------------------------------------------------------------------------------------- #

# 斷好的結果用「空白格（Space）」連接起來
cut_corpus = []
for i in word_segment:
    cut_corpus.append(' '.join(i))

for c in cut_corpus:
    # print (c)
    pass


text_cv = CountVectorizer(max_df=1.0, min_df=0.0)  # 某 term 出現在總文本的比率若超過 > 100% or < 0% 就剔除


td_matrix = text_cv.fit_transform(cut_corpus)


print(td_matrix.shape,"(文稿,關鍵字)")
# result >> (12,7)  # 12個句子(文本)，共提出7個關鍵字 # example

print(text_cv.vocabulary_.keys())

# print(text_cv.vocabulary_)  # result >> {'xxx':N, 'xxx':M, ...}
# print(sorted(text_cv.vocabulary_.items(), key=lambda x:x[1], reverse=True))  # result >> [('xxx':M, 'xxx':N, ...)]降冪排序(非couont數)
# result >> dict_keys(['韓國瑜', '夫婦', '房產', '韓氏', '雲林', '韓辦', '貸款'])

print(len(text_cv.vocabulary_.keys()))  # result >> 共提出幾個關鍵字數，數目
# result >> 7  # 儲存關鍵字的dictionary的長度(含有幾個元素)

# # ----------------------------------------------------------------------------------------------------------------------- #
# 以下測試出現錯誤，待調整。潛在應用: 了解優質業配文，使用這個關鍵字的權重
#idf指詞彙除以出現的文章數

# tfidf = TfidfTransformer()

# tfidf_matrix = tfidf.fit_transform(td_matrix)

# tfidf.idf_
# # result >> array([1.48550782, 1.48550782, 1.77318989, 1.77318989, 1.36772478, 1.61903921, 1.61903921])
        
# # ----------------------------------------------------------------------------------------------------------------------- #


import pandas as pd
df = pd.DataFrame(text_cv.vocabulary_)  
# print(df)


# # ----------------------------------------------------------------------------------------------------------------------- #
# # 計算每個關鍵字在data篇文本中的權重平均值
# keyword_row_mean = df.mean(axis=1)
# print(keyword_row_mean)

# ----------------------------------------------------------------------------------------------------------------------- #
# 將計算結果匯出為csv檔案

# Specify the name of the csv file
file_name = 'keywords_extraction_output.csv'  # 自訂檔名

# saving the excelsheet
df.to_csv(file_name)
print('Extracxted keywords successfully exported into csv File!')


