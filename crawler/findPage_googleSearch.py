from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, os



service = Service(executable_path="data/geckodriver.exe", log_path="NUL")
options = Options()

# 不跳實際的瀏覽器視窗出來(減少消耗無謂的效能)
# options.add_argument("--headless")
# 禁用通知
options.add_argument("--disable-notifications")

firefox= webdriver.Firefox(service=service, options=options)

# 隱含等待: 等待網頁載入完成後，再執行下面的程式，且只需設定一次，下面再有仔入網頁的動作時，無須再次設定，也會等待(最多20秒)網頁在入後再執行
firefox.implicitly_wait(20)


keyword= "保健食品"
# firefox.get("https://www.youtube.com/watch?v=aL9odRg3hyA")
firefox.get(f"https:www.google.com.tw/search?q={keyword}+site:www.facebook.com")
"https://www.facebook.com/hashtag/運動/"
f"https://duckduckgo.com/?q={keyword}+site:www.facebook.com"
f"https:www.google.com.tw/search?q={keyword}+site:www.facebook.com"

# 顯示等待
# WebDriverWait(firefox, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button'][@aria-label='關閉']"))).click()

# firefox.find_element(By.XPATH, "//div[@role='button'][@aria-label='關閉']").click()


last_update_page= ''
num=0
for x in range(10):
    firefox.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    
    time.sleep(1)


# soup= BeautifulSoup(firefox.page_source, "html.parser")
# 
# # firefox.quit()
# # print(soup.get_text().strip())
# results= soup.find_all('div', {"role":"article", "aria-describedby":True})
# for i,result in enumerate(results):
#     print(result.get_text().strip())
#     print(i, "-------")




