# 使用python-embed版時要加這2行
import sys, os, time, re
sys.path.append(os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
from db import *


# base_path= "/content/drive/Mydrive/.../page-Project/crawler"
base_path= os.path.abspath(os.path.dirname(__file__))




service = Service(executable_path=os.path.abspath(os.path.dirname(__file__)+"/data/geckodriver.exe"), log_path="NUL")
options = Options()

# 不跳實際的瀏覽器視窗出來(減少消耗無謂的效能)
# options.add_argument("--headless")
# 禁用通知
options.add_argument("--disable-notifications")

firefox= webdriver.Firefox(service=service, options=options)
# 隱含等待: 等待網頁載入完成後，再執行下面的程式，且只需設定一次，下面再有仔入網頁的動作時，無須再次設定，也會等待(最多10秒)網頁在入後再執行
firefox.implicitly_wait(5)
firefox.install_addon("data/return dislike/return_dislike.xpi", temporary=True)

if len(firefox.window_handles) > 1:
    for i,window in enumerate(firefox.window_handles):
        if i != 0:
            firefox.switch_to.window(window_name=window)
            firefox.close()
    firefox.switch_to.window(window_name=firefox.window_handles[0])


def getInfoFromYtUrl(url):
    firefox.get(url)
    # 確認title載入後，獲取title的文字
    title= WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.style-scope.ytd-watch-metadata")))
    title= title.get_attribute("textContent").strip() or ""
    
    # 確認description載入後，獲取description的文字(點開後才會有詳細的觀看次數)
    # 點擊展開說明欄，以獲取說明欄內完整文字
    WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tp-yt-paper-button#expand"))).click()
    description= WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-text-inline-expander")))
    # tag是yt-attributed-string的元素有2個，一個有id="attributed-snippet-text"，是剛進入時的說明欄。另一個沒有id，是展開後的說明欄
    description= description.find_element(By.CSS_SELECTOR, "yt-attributed-string:not(#attributed-snippet-text)")
    description= description.get_attribute("textContent").strip() or ""
    
    time.sleep(1)
    likes = firefox.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/ytd-segmented-like-dislike-button-renderer/yt-smartimation/div/div[1]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]')
    dislikes= WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/ytd-segmented-like-dislike-button-renderer/yt-smartimation/div/div[2]/ytd-toggle-button-renderer/yt-button-shape/button")))
    # dislikes= firefox.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/ytd-segmented-like-dislike-button-renderer/yt-smartimation/div/div[2]/ytd-toggle-button-renderer/yt-button-shape/button")
    views= firefox.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/div[1]/yt-formatted-string/span[1]")
    subscribers= firefox.find_element(By.XPATH, "//*[@id='owner-sub-count']")
    channel= firefox.find_element(By.XPATH, "//*[@id='text']/a")
    
    # channel_name, channel_id, subscribers, views, likes, dislikes
    return channel.text, channel.get_attribute("href").replace("https://www.youtube.com/",''), subscribers.text.replace("位訂閱者",""), views.text.replace("觀看次數：",'').replace("次",'').replace(",",''), likes.text, dislikes.text



# 新增欄位
updateCols("youtube", {"channel_name":"TEXT", "channel_ID":"TEXT", "subscribers":"INTEGER", "views":"INTEGER", "likes":"INTEGER", "dislikes":"INTEGER"})

data= getData("youtube", "SELECT id,link FROM youtube")
for row in data:
    row_id,link= row
    
    channel_name, channel_id, subscribers, views, likes, dislikes= getInfoFromYtUrl(link)
    if "萬" in subscribers: subscribers= int(float(subscribers.replace("萬",""))*10000)
    elif "億" in subscribers: subscribers= int(float(subscribers.replace("億",""))*100000000)
    
    updateData("youtube", {"channel_name":channel_name, "channel_id":channel_id, "subscribers":subscribers, "views":int(views), "likes":int(likes), "dislikes":int(dislikes)}, row_id)

# print(getInfoFromYtUrl("https://www.youtube.com/watch?v=aL9odRg3hyA"))