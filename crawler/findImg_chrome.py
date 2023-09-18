# 使用python-embed版時要加這2行
import sys, os, requests, base64
sys.path.append(os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from saveLink import *



keyword= "海洋垃圾"

service = Service(executable_path=os.path.abspath(os.path.dirname(__file__)+"/data/chromedriver.exe"))
options = Options()

# 不跳實際的瀏覽器視窗出來(減少消耗無謂的效能)
# options.add_argument("--headless")
# 禁用通知
options.add_argument("--disable-notifications")
options.add_experimental_option("excludeSwitches", ["disable-logging"])

chrome= webdriver.Chrome(service=service, options=options)
# 隱含等待: 等待網頁載入完成後，再執行下面的程式，且只需設定一次，下面再有仔入網頁的動作時，無須再次設定，也會等待(最多10秒)網頁在入後再執行
chrome.implicitly_wait(1)



chrome.get(f"https://www.google.com.tw/search?q={keyword}&source=lnms&tbm=isch&sa")



imgLinks= []
imgFile= os.path.abspath(os.path.dirname(__file__)+"/data/images")
os.makedirs(imgFile, exist_ok=True)
lastFileNum= os.listdir(imgFile)
if lastFileNum:
    lastFileNum= int(lastFileNum[-1].split("."))
else:
    lastFileNum= 0



# 如果第一批連結的數量少於100，則往下捲動，載入更連結後再重新拿一次第一批連結，最多捲動100次
for i in range(100):
    if len(imgLinks) >= 100:
        break
    
    
    imgElements= WebDriverWait(chrome, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.rg_i.Q4LuWd[src]")))
    newImgLinks= [imgElement.get_attribute("src") for imgElement in imgElements if imgElement.get_attribute("src") not in imgLinks]
    imgLinks+= newImgLinks
    
    if len(chrome.find_elements(By.CSS_SELECTOR, "input[jsaction='Pmjnye2']")) >0:
        chrome.find_element(By.CSS_SELECTOR, "input[jsaction='Pmjnye2']").click()
    
    chrome.execute_script("window.scrollTo(0,document.querySelector('#islmp').scrollHeight)")
    
    
    for newImgLink in newImgLinks:
        try:
            if newImgLink.startswith("http"):
                image= requests.get(newImgLink).content
            else:
                image = base64.b64decode(newImgLink.split(',')[-1], validate=True)
            
            with open(imgFile+ f"/{lastFileNum}.jpg", "wb") as f:
                
                f.write(image)
            lastFileNum+= 1
        except: pass
# print(imgLinks)






