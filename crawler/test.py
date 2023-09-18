# import sys, os
# sys.path.append(os.path.dirname(__file__))


# import jieba

# jieba.set_dictionary('dict.txt.big')


from bs4 import BeautifulSoup
soup= BeautifulSoup("<div>hello</div>", "html.parser")
print(soup.get_text())