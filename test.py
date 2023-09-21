# import sys, os
# sys.path.append(os.path.dirname(__file__))


# import jieba

# jieba.set_dictionary('dict.txt.big')


# import re
# 
# print(re.search("()","hell2o world"))
# print(re.search("z","ho1w are you"))




db2_path= "crawler/data/data.db"



import os, sqlite3


base_path= os.path.abspath(os.path.dirname(__file__))


# 取得db2的資料
conn = sqlite3.connect(os.path.join(base_path,db2_path))
cursor= conn.cursor()
result= cursor.execute("SELECT title,description,link FROM youtube WHERE link='aa'")
data2= result.fetchone()
print(data2)