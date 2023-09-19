# import sys, os
# sys.path.append(os.path.dirname(__file__))


# import jieba

# jieba.set_dictionary('dict.txt.big')


import re

print(re.search("[hello|hey]","hello world"))
print(re.search("how.*you","ho1w are you"))
