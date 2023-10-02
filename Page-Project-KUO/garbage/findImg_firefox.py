# 使用python-embed版時要加這2行
import sys, os, requests, base64
sys.path.append(os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from saveLink import *



keyword= "釣竿"
file_prefix= "waste_13_"


service = Service(executable_path=os.path.abspath(os.path.dirname(__file__)+"/data/geckodriver.exe"), log_path="NUL")
options = Options()

# 不跳實際的瀏覽器視窗出來(減少消耗無謂的效能)
# options.add_argument("--headless")
# 禁用通知
options.add_argument("--disable-notifications")

firefox= webdriver.Firefox(service=service, options=options)
# 隱含等待: 等待網頁載入完成後，再執行下面的程式，且只需設定一次，下面再有仔入網頁的動作時，無須再次設定，也會等待(最多10秒)網頁在入後再執行
firefox.implicitly_wait(1)



firefox.get(f"https://www.google.com.tw/search?q={keyword}&source=lnms&tbm=isch&sa")



imgLinks= []
imgFile= os.path.abspath(os.path.dirname(__file__)+"/data/images")
os.makedirs(imgFile, exist_ok=True)
lastFileNum= os.listdir(imgFile)
if lastFileNum:
    lastFileNum= len(lastFileNum)
else:
    lastFileNum= 0
nowNum= 0


# 如果第一批連結的數量少於100，則往下捲動，載入更連結後再重新拿一次第一批連結，最多捲動100次
for i in range(1000):
    if len(imgLinks) >= 1000:
        break
    
    
    imgElements= WebDriverWait(firefox, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.rg_i.Q4LuWd[src]")))
    newImgElements= [imgElement for imgElement in imgElements if imgElement.get_attribute("src") not in imgLinks]
    imgLinks+= [imgElement.get_attribute("src") for imgElement in newImgElements]
    
    if len(firefox.find_elements(By.CSS_SELECTOR, "input[jsaction='Pmjnye2']")) >0:
        firefox.find_element(By.CSS_SELECTOR, "input[jsaction='Pmjnye2']").click()
    
    firefox.execute_script("window.scrollTo(0,document.querySelector('#islmp').scrollHeight)")
    
    
    for newImgElement in newImgElements:
        try:
            newImgElement.click()
            newImgLink= WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.r48jcc.pT0Scc.iPVvYb[jsaction="VQAsE"][jsname="kn3ccd"]'))).get_attribute("src")
            if newImgLink.startswith("http"):
                image= requests.get(newImgLink).content
            else:
                image = base64.b64decode(newImgLink.split(',')[-1], validate=True)
            
            with open(imgFile+ f"/{file_prefix}{lastFileNum}.jpg", "wb") as f:
                
                f.write(image)
            lastFileNum+= 1
        except: pass
# print(imgLinks)






