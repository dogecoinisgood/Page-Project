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
'''
【本片即將開始】【請先關注訂閱、分享、按鈴鐺】注意看,這個女人實在太狠了既然說是想要仿妝比美這個奇怪的女子穿著紅白條紋不知道是去哪找來的衣服那麼就開始吧這個Kai Beauty這個透亮妝前乳不知道是幹什麼的想必是妝前先上一層的乳吧看起來反光就是這樣然後拿這個畫櫃這樣子有沒有看出來左邊是after右邊是before這樣有看到嗎下一個遮瑕膏把髒髒的地方都蓋起來R2是射擊鈕看到不好就把它蓋下去右邊也滿滿滿滿滿滿下一個這個粉底露跟精華粉底精華Kai你有沒有看到這邊也補一層舒服舒服拿這個奶油刀這樣子抹在臉上然後再來粉撲撲額頭也給它蓋一層人中不要忘記上髮很棒你看看得到嗎看不到的話我們再更近一點看一下你看有看到吧這個是什麼這個誰彩筆是高中的時候留到現在終於可以派上用場了你有沒有看到我再講一看第三次看到這邊的水美眉你們都有福了你們就照著我這樣子美美美啪啪啪就可以像我一樣美麗了你看有沒有看到然後這個是不一樣的粉紅色是不是比較好看等一下問你男朋友一定不知道這個粉紅色差別在哪裡你們看是不是很漂亮I'm a Barbie girlIn the Barbie world再來是裸光蜜粉欸左邊撲撲右邊也撲撲漂亮再來這個三色修容餅到底要修幾次呢你看是不是before after又不一樣了讚中間的修容到底是差別在哪裡呢右邊刷刷上面也刷刷然後眉毛不要浪費也刷刷再來顏彩盤這個就是拿來畫眼睛的有沒有看到這四個顏色我現在用的是第一個Pink Pinky畫我的漂亮眼睛你是不是看到眼睛裡面有光第二個眼皮也要有光我說眼皮有光就有光下面的眼皮也不要忘記也要有光喔漂亮不知道看哪裡第四種的粉紅色粉紅色Pinky這個是斐濟貝一樣的妝容感讓大家知道我們非常的新鮮Fresh這個臥蠶棒這個不是拿來按摩的這個是拿來畫我們的臥蠶的你看這樣笑起來才會有肌肉這樣子稍微縮起來笑得很開心的感覺我沒有在笑你就感覺我在笑你看我的網美手這個是拿來畫眉毛的你看這樣刷上去是不是好方便這個是橡皮擦嗎這個是Beauty什麼不知道在幹嘛的刷眉毛的你看我的眉毛這樣是不是很有神魔法來囉Before跟After都一樣了不要看我的手看這個是眼線液筆溫柔中我們看這個有多溫柔你要這樣輕輕的畫你看是不是越來越溫柔了呢暴力之氣都不見了下面也要用溫柔中畫一下鼻孔太大了各位觀眾我們的工程現在已經快要接近到尾聲了我們把這個睫毛再給它收尾夾翹一下不要夾錯不要夾到眼皮再用睫毛膏幫我們的睫毛定型你有看過那個蟑螂腳吧就是把它畫成像蟑螂腳那樣子長長的然後我也不知道為什麼要把我的睫毛這樣一束一束的把它夾起來可能真的有比較漂亮吧你說呢Baby你看我的眼睛是不是很漂亮怎麼了你終於看不清楚過來化妝一輩子不小心沾到了然後再拿我這個國小流盛的水彩筆在我的眼睛上方還有我的顴骨上方都刷亮刷亮看起來更有精神還有嘴唇這好滑順喔哪裡都可以擦擦的然後這個嘴巴這樣blend blend的再加強剛剛忘記畫了這邊也再畫一點為什麼大家上幾種唇色這看起來不小心咬到自己嘴巴一樣怎麼突然變成櫻桃色了呢Magic我們這次真的要進入到最後尾聲了你看最後的上光像果凍一樣你以為這樣就完了嗎沒有脖子也不能忘記了你以為這樣就結束了還有帶上我們奇怪的墨鏡漂亮蘋果肌愛心愛心金妮亞帶上墨鏡就完成了喜歡的話請訂閱支持啊還有分享出去我們下次再見掰掰by bwd6
'''



model_name= "distiluse-base-multilingual-cased-v2"
# model_name= "paraphrase-distilroberta-base-v1"
model_path= os.path.abspath(os.path.join(base_path, "data/sentence-transformers", model_name))

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

diss= sorted(diss, reverse=True)[:10]
print(sum(diss)/len(diss))
