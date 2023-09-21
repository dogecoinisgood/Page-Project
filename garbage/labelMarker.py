import xml.etree.ElementTree as ET
import xml.dom.minidom
import numpy as np
import pandas as pd
import os, cv2, time, threading



# 操作說明
# 滑鼠左鍵: 拉框
# 滑鼠右鍵: 清除所有的框
# b: 上一張圖片(&自動儲存)
# n: 下一張圖片(&自動儲存)
# s: 儲存現在化的眶的座標到xml
# d: 刪除現在的圖片
# f: (預定)自動填充沙灘背景
# Esc: 關閉視窗
# 
# 
# 要標記的圖片記得放在data/images資料夾內
# dataset_10000_update_0912.xml記得要放在data資料夾中





# 指定從哪個檔案開始，若沒設定，則為從低一張沒有標記的圖片開始
target_file= "waste_30_10你好.jpg"



base_path= os.path.abspath(os.path.dirname(__file__))

# 從檔案載入並解析 XML 資料
tree = ET.parse(base_path+"/data/dataset_10000_update_0912.xml")
root = tree.getroot()


# # XML ot DataFrame
# {"name":name1, "width":"10", "height":"10", "polygon": [{"WASTE_1":"xx,xx..."}, {"WASTE_2":"yy,yy..."}]}
df= pd.DataFrame([
        [image.attrib["name"], image.attrib["width"], image.attrib["height"], [{polygon.attrib["label"]:polygon.attrib["points"]} for polygon in image]]
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
        if image not in df["name"].values:
            nowImageNum= i
            break
# 讀取目標的圖片
# img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)
img= cv2.imdecode(np.fromfile((base_path+'/data/images/'+unMarkImages[nowImageNum]), dtype=np.int8), -1)


# 紀錄左鍵按下，開始拖曳時的點
dragPoint= None
# 紀錄同一張圖的其他框, rectangles= [{"WASTE_1":"xx,xx..."}, {"WASTE_2":"yy,yy..."}]
rectangles= []
def showRectangles():
    global rectangles, img
    # img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)
    img= cv2.imdecode(np.fromfile((base_path+'/data/images/'+unMarkImages[nowImageNum]), dtype=np.int8), -1)
    cv2.setWindowTitle('image', unMarkImages[nowImageNum])
    for polygon in rectangles:
        label, points= list(polygon.keys())[0], list(polygon.values())[0]
        # start, end= points
        # cv2.rectangle(img, start, end, (0,255,0), 2)
        cv2.polylines(img, points, 1, (0, 255, 0), 5)
        cv2.putText(img, label, points[0][0], None, 0.75,(255,255,255),3)
        cv2.putText(img, label, points[0][0], None, 0.75,(0,0,255), 2)


def readRectanglesFromDf():
    global df, nowImageNum, rectangles
    newSeries= df.loc[df['name'] == unMarkImages[nowImageNum]]
    rectangles= []
    if not newSeries.empty:
        newSeries= newSeries.iloc[0]
        for polygon in newSeries['polygon']:
            label, points= list(polygon.keys())[0], list(polygon.values())[0]
            # p0, _, _, p3= points.split(";")
            # p0, p3= (int(p0.split(",")[0]), int(p0.split(",")[1])), (int(p3.split(",")[0]), int(p3.split(",")[1]))
            # rectangles.append({label:[p0, p3]})
            rectangles.append({label: np.array([[[dot for dot in point.split(",")] for point in points.split(";")]], dtype=np.int32)})
    showRectangles()
readRectanglesFromDf()


nowLabel= "WASTE_1"
#滑鼠事件
def OnMouseAction(event,x,y,flags,param):
    global dragPoint, img, rectangles, nowLabel
    
    # 左鍵按下
    if event == cv2.EVENT_LBUTTONDOWN:
        dragPoint= [x,y]
    # 左鍵放開
    elif event == cv2.EVENT_LBUTTONUP:
        # 紀錄畫下的框
        # rectangles.append({nowLabel:[(dragPoint[0],dragPoint[1]), (x,y)]})
        rectangles.append({nowLabel:np.array([[[dragPoint[0],dragPoint[1]], [x,dragPoint[1]], [x,y], [dragPoint[0],y]]],dtype=np.int32)})
        showRectangles()
        # 重設開始座標
        dragPoint= None
    # 左鍵拖曳
    elif flags==cv2.EVENT_FLAG_LBUTTON:
        # 在按下滑鼠拖曳的時候，要隨時更新背景的圖片，以消除前一貞畫下的框
        showRectangles()
        cv2.rectangle(img, (dragPoint[0],dragPoint[1]), (x,y), (0,255,0), 2)
    # 右鍵按下
    elif event==cv2.EVENT_RBUTTONDOWN :
        # 重設同一張圖之前紀錄下來的其他框
        rectangles= []
        showRectangles()


# 儲存文件
def saveXML():
    global img, rectangles, df, nowImageNum, tree, root
    
    imgElement= ET.fromstring(f'<image name="{unMarkImages[nowImageNum]}" height="{img.shape[0]}" width="{img.shape[1]}"></image>')
    newDict= {"name":unMarkImages[nowImageNum],"width":img.shape[1],"height":img.shape[0], "polygon":[]}
    for polygon in rectangles:
        label, points= list(polygon.keys())[0], list(polygon.values())[0]
        # start, end= points
        # polygonElement= ET.fromstring(f'<polygon label="{label}" points="{start[0]},{start[1]};{start[0]},{end[1]};{end[0]},{start[1]};{end[0]},{end[1]}" />')
        points= [f"{point[0]},{point[1]}" for point in points[0]]
        polygonElement= ET.fromstring(f'<polygon label="{label}" points="{";".join(points)}" />')
        imgElement.insert(-1, polygonElement)
        # newDict["polygon"].append({label: f"{start[0]},{start[1]};{start[0]},{end[1]};{end[0]},{start[1]};{end[0]},{end[1]}"})
        newDict["polygon"].append({label: f"{';'.join(points)}"})
    
    nowSeries= df.loc[df['name'] == unMarkImages[nowImageNum]]
    if nowSeries.empty:
        df.loc[len(df)] = newDict
        root.insert(-1, imgElement)
    else:
        idx= df.index[df['name'] == unMarkImages[nowImageNum]].tolist()[0]
        df['polygon'].iat[idx]= newDict['polygon']
        root[idx]= imgElement
    tree.write(base_path+"/data/dataset_10000_update_0912.xml")


def deleteImg():
    global unMarkImages, nowImageNum, df, root, tree
    try:
        os.remove(base_path+ "/data/images/"+ unMarkImages[nowImageNum])
    except: pass
    
    nowSeries= df.loc[df['name'] == unMarkImages[nowImageNum]]
    if not nowSeries.empty:
        idx= df.index[df['name'] == unMarkImages[nowImageNum]].tolist()[0]
        df= df.drop([idx])
        root.remove(root[idx])
        tree.write(base_path+"/data/dataset_10000_update_0912.xml")
    # 最後才將unMarkImages裡的fileName給dump掉，避免pandas和XML抓取index時發生錯誤
    unMarkImages.pop(nowImageNum)
    readRectanglesFromDf()


# 上/下一張圖片
def changeImg(x):
    global nowImageNum
    
    if x == -1:
        nowImageNum= nowImageNum-1 if nowImageNum>0 else 0
    elif x == 1:
        nowImageNum= nowImageNum+1 if (nowImageNum<len(unMarkImages)-1) else len(unMarkImages)-1
    cv2.setTrackbarPos('<-\t->', 'image', 0)
    readRectanglesFromDf()


# 更改label
def changeLabel(x):
    global nowLabel
    nowLabel= f"WASTE_{x}"



cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setWindowTitle('image', unMarkImages[nowImageNum])
cv2.setMouseCallback('image',OnMouseAction)
cv2.createTrackbar('<-\t->','image',0,1, changeImg)
cv2.setTrackbarMin('<-\t->', 'image', -1)
cv2.createTrackbar('label','image',1,20, changeLabel)
cv2.setTrackbarMin('label', 'image', 1)
while(img.size!=0):
    key= cv2.waitKey(1)&0xFF
    if key == ord('s'):
        saveXML()
    elif key == ord('d'):
        deleteImg()
    elif key == ord('n'):
        changeImg(1)
    elif key == ord('b'):
        changeImg(-1)
    elif key == ord('f'):
        pass
    elif key==27:
        break
    try:
        cv2.imshow('image',img)
    except:
        img = np.zeros((500,500,3),np.uint8)
        cv2.imshow('image',img)
cv2.destroyAllWindows()