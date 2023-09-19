# 使用python-embed版時要加這2行
import sys, os, time, re
sys.path.append(os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from saveLink import *



keywords= "口紅"
keywords2= ""
firstSearchResult= 100
relatedStack= 100


service = Service(executable_path=os.path.abspath(os.path.dirname(__file__)+"/data/geckodriver.exe"), log_path="NUL")
options = Options()

# 不跳實際的瀏覽器視窗出來(減少消耗無謂的效能)
options.add_argument("--headless")
# 禁用通知
options.add_argument("--disable-notifications")

firefox= webdriver.Firefox(service=service, options=options)
# 隱含等待: 等待網頁載入完成後，再執行下面的程式，且只需設定一次，下面再有仔入網頁的動作時，無須再次設定，也會等待(最多10秒)網頁在入後再執行
firefox.implicitly_wait(10)



firefox.get(f"https://www.youtube.com/results?search_query={keywords+keywords2}")

# 從搜尋結果獲取第一批連結
def getFirstLinks():
    # 等到所有<ytd-video-renderer>元素載入
    firstLinks= WebDriverWait(firefox, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "ytd-video-renderer")))
    # 尋找所有<ytd-video-renderer>中，所有的<a id="thumbnail">元素，並取得這些元素中的連結內容
    firstLinks= [firstLink.find_element(By.CSS_SELECTOR,"a#thumbnail").get_attribute("href") for firstLink in firstLinks]
    # 篩選掉連結不符合要求的
    firstLinks= [firstLink for firstLink in firstLinks if firstLink!=None and (firstLink.startswith("https://www.youtube.com/watch?") or firstLink.startswith("/watch?"))]
    return firstLinks

firstLinks= getFirstLinks()

# 如果第一批連結的數量少於100(firstSearchResult設定的數字)，則往下捲動，載入更連結後再重新拿一次第一批連結，最多捲動100(firstSearchResult設定的數字)次
for i in range(firstSearchResult):
    if len(firstLinks) >= firstSearchResult:
        break
    body= WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-app")))
    firefox.execute_script("window.scrollTo(0,document.querySelector('ytd-app').scrollHeight)")
    firstLinks= getFirstLinks()



# 候選連結名單: 跑過的。以及已經抓到，但還沒跑的連結。避免一直跑重複的網頁
candidates= []+ firstLinks

def findRelated(href ,num:int):
    # 篩選掉含有時間戳的部分
    if "&t=" in href:
        href= href.split("&t=")[0]
    # 確認此連結不在資料庫裡
    
    if num>0 and getData("youtube", "SELECT link FROM youtube WHERE link='{}';".format(href.replace("'", "''")))==[]:
        try:
            firefox.get(href)
            # 確認title載入後，獲取title的文字
            title= WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.style-scope.ytd-watch-metadata")))
            title= title.get_attribute("textContent").strip() or ""
            
            # 確認description載入後，獲取description的文字
            # 點擊展開說明欄，以獲取說明欄內完整文字
            WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tp-yt-paper-button#expand"))).click()
            description= WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-text-inline-expander")))
            # tag是yt-attributed-string的元素有2個，一個有id="attributed-snippet-text"，是剛進入時的說明欄。另一個沒有id，是展開後的說明欄
            description= description.find_element(By.CSS_SELECTOR, "yt-attributed-string:not(#attributed-snippet-text)")
            description= description.get_attribute("textContent").strip() or ""
            
            print(title)
            print("----")
            
            # 如果title或description中有包含關鍵字，就儲存到資料庫，並開始找相關連結
            reStr= f"[{'|'.join(keywords.split())}]"
            reStr2= f"[{'|'.join(keywords2.split())}]"
            if re.search(reStr, title+description) and re.search(reStr2, title+description):
                insertData("youtube", {"title":title, "description":description, "link": href})
                
                # 開始找右邊相關影片的其他連結
                results= WebDriverWait(firefox, 10).until(EC.presence_of_element_located((By.ID, "secondary")))
                results= results.find_elements(By.TAG_NAME, "a")
                results= [result.get_attribute("href") for result in results]
                # 篩選掉含有時間戳的網址(大該率是同一部影片的不同時間而已)
                results= [result for result in results if result!=None and "www.youtube.com/watch?" in result and '&t=' not in result]
                
                
                for result in results:
                    if result not in candidates:
                        time.sleep(0.2)
                        candidates.append(result)
                        findRelated(result, num-1)
        except:
            return

    # firefox.quit()


# 分別進入第一批連結，並取得資料與下一批連結
for i,firstLink in enumerate(firstLinks):
    print("---", i, "/", len(firstLinks), "---")
    findRelated(firstLink, relatedStack)
    




