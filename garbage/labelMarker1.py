import xml.etree.ElementTree as ET
import xml.dom.minidom
import numpy as np
import pandas as pd
import os, cv2, time, threading

#123測試

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
target_file= "20221208_新北市_福隆-234.jpg" #5426



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
unMarkImages= sorted(os.listdir(base_path+"/data/images"))
# 如果有寫target_file，則直接抓取該檔案的index，並從該張圖片開始
if target_file:
    nowImageNum= unMarkImages.index(target_file)
else:
    # 否則找到所有放在待標記資料夾的圖片中，第一個沒有標記的圖片編號
    nowImageNum= 0
    for i,image in enumerate(unMarkImages):
        if image not in df["name"].values:
            nowImageNum= i
            break

# 讀取目標的圖片 (棄用，因為後面在showRectangles()讀取框的時候，會在)
# img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)
# img= cv2.imdecode(np.fromfile((base_path+'/data/images/'+unMarkImages[nowImageNum]), dtype=np.int8), -1)


# 紀錄左鍵按下，開始拖曳時的點
dragPoint= None
# 紀錄同一張圖的其他框, rectangles= [{"WASTE_1":np.array([[[x1,y1],[x2,y2], ...]])}, {"WASTE_2":[[]]...}]
rectangles= []
def showRectangles():
    global rectangles, img
    # img = cv2.imread((base_path+'/data/images/'+unMarkImages[nowImageNum]), cv2.IMREAD_COLOR)
    # 用imread會無法讀取有中文的路徑，所以用np讀取該圖片轉成np.array，在丟到cv2.imdecode讀取
    img= cv2.imdecode(np.fromfile((base_path+'/data/images/'+unMarkImages[nowImageNum]), dtype=np.int8), -1)
    cv2.setWindowTitle('image', unMarkImages[nowImageNum])
    for polygon in rectangles:
        label, points= list(polygon.keys())[0], list(polygon.values())[0]
        # 原始資料在四邊形時的順序多為(左上,左下,右上,右下)，所以做特別處理(預定)
        # if len(points) == 4:
        #     cv2.rectangle(img, )
        # else:
        cv2.polylines(img, points, 1, (0, 255, 0), 5)
        cv2.putText(img, label, points[0][0], None, 0.75,(255,255,255),3)
        cv2.putText(img, label, points[0][0], None, 0.75,(0,0,255), 2)


def readRectanglesFromDf():
    global df, nowImageNum, rectangles
    # 先嘗試搜尋dataFrame中有沒有現在正在看的圖片
    newSeries= df.loc[df['name'] == unMarkImages[nowImageNum]]
    rectangles= []
    # 有的話就讀取
    if not newSeries.empty:
        newSeries= newSeries.iloc[0]
        # 讀取這筆資料中的所有label和label的座標位置
        for polygon in newSeries['polygon']:
            label, points= list(polygon.keys())[0], list(polygon.values())[0]
            # 格式為: {"WASTE_1":np.array([[[x1,y1],[x2,y2], ...]])}
            rectangles.append({label: np.array([[[dot for dot in point.split(",")] for point in points.split(";")]], dtype=np.int32)})
    # 讀取完之後記得顯示出所有的框框和label名
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
        # rectangles格式為: {"WASTE_1":np.array([[[x1,y1],[x2,y2], ...]])}
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
    
    # 建立一個XML的image元素。並建立一個dict以利後續在dataFrame的新增資料
    imgElement= ET.fromstring(f'<image name="{unMarkImages[nowImageNum]}" height="{img.shape[0]}" width="{img.shape[1]}"></image>')
    newDict= {"name":unMarkImages[nowImageNum],"width":img.shape[1],"height":img.shape[0], "polygon":[]}
    for polygon in rectangles:
        label, points= list(polygon.keys())[0], list(polygon.values())[0]
        # points= np.array([[[x1,y1],[x2,y2], ...]]) => ["x1,y1", "x2,y2", ...]
        points= [f"{point[0]},{point[1]}" for point in points[0]]
        polygonElement= ET.fromstring(f'<polygon label="{label}" points="{";".join(points)}" />')
        # 在image元素的最後面，插入一個polygon
        imgElement.insert(-1, polygonElement)
        newDict["polygon"].append({label: f"{';'.join(points)}"})
    
    # 先嘗試搜尋dataFrame中有沒有現在正要儲存的圖片
    nowSeries= df.loc[df['name'] == unMarkImages[nowImageNum]]
    # 如果沒有的話，就插在dataFrame/XML裡面
    if nowSeries.empty:
        df.loc[len(df)] = newDict
        root.insert(-1, imgElement)
    # 有的話，先找到這筆資料在df裡面的idx，再更改該筆資料
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
    global unMarkImages,nowImageNum
    
    # 避免cv2.setTrackbarPos(.., .., 0)的時候，又觸發一次此函式。
    if x == 0:
        return
    
    if x == -1:
        nowImageNum= nowImageNum-1 if nowImageNum>0 else 0
    elif x == 1:
        nowImageNum= nowImageNum+1 if (nowImageNum<len(unMarkImages)-1) else len(unMarkImages)-1
    
    cv2.setTrackbarPos('<-\t->', 'image', 0)
    readRectanglesFromDf()
    print(nowImageNum, unMarkImages[nowImageNum])


# 更改label
def changeLabel(x):
    global nowLabel
    nowLabel= f"WASTE_{x}"



cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setWindowTitle('image', unMarkImages[nowImageNum])
cv2.setMouseCallback('image',OnMouseAction)
cv2.createTrackbar('<-\t->','image',0,1, changeImg)
cv2.setTrackbarMin('<-\t->', 'image', -1)
cv2.createTrackbar('label','image',1,21, changeLabel)
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