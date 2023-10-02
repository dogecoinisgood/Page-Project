# import sys, os
# sys.path.append(os.path.dirname(__file__))


# import jieba

# jieba.set_dictionary('dict.txt.big')


import re

print(re.search("()","hell2o world"))
print(re.search("z","ho1w are you"))

print(re.search("(ho|1w)","ho1w are you"))
print(re.search("(xx|.*)","ho1w are you"))


print("1.23".isdigit())

