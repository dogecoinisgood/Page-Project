import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import os, cv2, time, threading



label= ""
target_file= ""

base_path= os.path.abspath(os.path.dirname(__file__))

# 從檔案載入並解析 XML 資料
tree = ET.parse(base_path+"/data/dataset_10000_update_0912.xml")
root = tree.getroot()


# # XML ot DataFrame
# {"name":name1, "width":"10", "height":"10", "polygon": [{"label":"WASTE_1","points":"xx,xx..."}, {"label":"WASTE_2","points":"yy,yy..."}]}
df= pd.DataFrame([
        [image.attrib["name"], image.attrib["width"], image.attrib["height"], [{"label":polygon.attrib["label"], "points":polygon.attrib["points"]} for polygon in image]]
    for image in root],
    columns=["name","width","height","polygon"]
)


# 找到所有放在待標記資料夾的圖片
unMarkImages= os.listdir(base_path+"/data/images")
if target_file:
    nowImageNum= unMarkImages.index(target_file)
else:
    # 找到所有放在待標記資料夾的圖片中，第一個沒有標記的圖片編號
    nowImageNum= 0
    for i,image in enumerate(unMarkImages):
        if image not in df["name"]:
            nowImageNum= i
            break
# 讀取目標的圖片
img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)


# 紀錄左鍵按下，開始拖曳時的點
dragPoint= None
# 紀錄同一張圖的其他框
rectangles= []
#建立回调函数
def OnMouseAction(event,x,y,flags,param):
    global mousePressing, dragPoint, img, rectangles
    
    # 左鍵按下
    if event == cv2.EVENT_LBUTTONDOWN:
        dragPoint= [x,y]
    # 左鍵放開
    elif event == cv2.EVENT_LBUTTONUP:
        # 紀錄畫下的框
        rectangles.append([(dragPoint[0],dragPoint[1]), (x,y)])
        # 重設開始座標
        dragPoint= None
    # 左鍵拖曳
    elif flags==cv2.EVENT_FLAG_LBUTTON:
        # 在按下滑鼠拖曳的時候，要隨時更新背景的圖片，以消除前一貞畫下的框
        img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)
        for start,end in rectangles:
            cv2.rectangle(img, start, end, (0,255,0), 2)
        cv2.rectangle(img, (dragPoint[0],dragPoint[1]), (x,y), (0,255,0), 2)
    # 右鍵按下
    elif event==cv2.EVENT_RBUTTONDOWN :
        # 重設同一張圖之前紀錄下來的其他框
        rectangles= []
        img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)


# 儲存文件
def saveXML():
    global img, rectangles, df, nowImageNum, tree, root
    
    imgElement= ET.fromstring('<image name="{unMarkImages[nowImageNum]}" height="{img.shape[0]}" weight="{img.shape[1]}"></image>')
    newDict= {"name":unMarkImages[nowImageNum],"width":img.shape[1],"height":img.shape[0], "polygon":[]}
    for start,end in rectangles:
        polygonElement= ET.fromstring('<polygon label="{label}" points="{start[0]},{start[1]};{start[0]},{end[1]};{end[0]},{start[1]};{end[0]},{end[1]}" />')
        imgElement.insert(polygonElement, "polygon")
        newDict["polygon"].append({"label": label, "points":f"{start[0]},{start[1]};{start[0]},{end[1]};{end[0]},{start[1]};{end[0]},{end[1]}"})
        
    df= pd.concat([df, pd.Series(newDict)])
    root.insert(imgElement, "image")
    
    # 重設所有的框，並自動跳到下一張
    rectangles= []
    nowImageNum+= 1
    img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)



# 上/下一張圖片
def changeImg(x):
    global nowImageNum, img
    if x == -1:
        nowImageNum= nowImageNum-1 if nowImageNum>0 else 0
    elif x == 1:
        nowImageNum= nowImageNum+1 if (nowImageNum<len(unMarkImages)-1) else len(unMarkImages)-1
    cv2.setTrackbarPos('<-\t->', 'image', 0)
    img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)
    cv2.setWindowTitle('image', unMarkImages[nowImageNum])



cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setWindowTitle('image', unMarkImages[nowImageNum])
cv2.setMouseCallback('image',OnMouseAction)
cv2.createTrackbar('<-\t->','image',0,1, changeImg)
cv2.setTrackbarMin('<-\t->', 'image', -1)
while(img.size!=0):
    key= cv2.waitKey(1)&0xFF
    if key == ord('s'):
        saveXML()
    if key==27:
        break
    try:
        cv2.imshow('image',img)
    except:
        img = np.zeros((500,500,3),np.uint8)
        cv2.imshow('image',img)
cv2.destroyAllWindows()