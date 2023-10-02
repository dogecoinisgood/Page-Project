import os, re
import cv2
from PIL import Image
import xml.etree.ElementTree as ET
from xml.dom import minidom 

#把file的路徑改成絕對路徑後把目錄中所有檔案用list格式印出
imgs = os.listdir(os.path.abspath(os.path.dirname(__file__))+'/garbageImg/Syringe/Syringe2\test\train/images') 
# root = ET.Element("annotations")建立新的檔案
#讀取文件
tree = ET.parse("garbageXml/dataset_10000_update_0912.xml")
#讀取文件的根目錄
root = tree.getroot()

for img in imgs:
    #圖片path
    img2 = cv2.imread('D:/Page-Project-Che/crawler/garbageImg/Lighter/Lighter/train/images/'+img)
    #imgH=圖高,imgW=圖寬,顏色用不到
    imgH, imgW, color = img2.shape
    #label path + .jpg取代為.txt =>命名為txt
    with open('D:/Page-Project-Che/crawler/garbageImg/Lighter/Lighter/train/labels/'+img.replace(".jpg",".txt")) as txt:
        #讀檔
        txtContnet= txt.read()
        element1 = ET.fromstring(f'<image height="{imgH}" name="{img}" width="{imgW}"></image>')
        root.append(element1)
        #txtContnet:"0 0.123 0.456 0.789 \n 0 0.123 0.456 0.789 ..."換行切出字串
        for row in txtContnet.split('\n'):
            # row: "0 0.123 0.456 0.789 ..." => [0, 0.123, 0.456 0.789, ...]字串切出字
            row= [float(value) for value in row.split()] 
            #因為第一項是label的class不需要，所以取1:4
            right,left,top,bottom= row[1:]
            #right=right(%)*imgW
            right, left= int(right*imgW), int(left*imgW)
            top,bottom= int(top*imgH), int(bottom*imgH)
            #label="244,135;244,150;123,135;123,150"
            label= f"{left},{top};{left},{bottom};{right},{top};{right},{bottom}" 
            element2 = ET.fromstring(f'<polygon label="WASTE_19" points="{label}" />')
            element1.append(element2)
            print(imgH ,img ,imgW,label)

#把root->object<class:document>
dom= minidom.parseString(ET.tostring(root, method='xml', encoding='utf-8'))
with open(os.path.dirname(__file__)+'/garbageXml/dataset_10000_update_09222.xml', "w", encoding='utf-8') as f:
    # 將dom.toprettyxml()(->string)中所有'\n[0~n個空白]\n'替換成一個\n
    f.write(re.sub('\n\W*\n','\n',dom.toprettyxml(encoding='utf-8').decode()))
