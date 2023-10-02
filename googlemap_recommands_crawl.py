from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
import random

# url = "要爬取的餐廳google評論連結"
url = 'https://www.google.com/maps/place/%E8%B5%B7%E5%AE%B6%E9%9B%9E%E9%9F%93%E5%BC%8F%E7%82%B8%E9%9B%9E+%E4%B8%AD%E6%AD%A3%E5%AF%A7%E6%B3%A2%E5%BA%97/@25.0320312,121.515924,17z/data=!3m1!5s0x3442a99eb5700fc7:0x4c531857fded6ce4!4m18!1m9!3m8!1s0x3442a99eb59cabfb:0xd9cf9cd1992ceb6c!2z6YeR5bOw6a2v6IKJ6aOv!8m2!3d25.0320264!4d121.5184989!9m1!1b1!16s%2Fg%2F1tj98pyk!3m7!1s0x3442a9c0f220e033:0x7ded85af933c4f95!8m2!3d25.0311643!4d121.5180751!9m1!1b1!16s%2Fg%2F11h7ftcyv3?hl=zh-TW&entry=ttu'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)
data = driver.page_source
soup = BeautifulSoup(data,'html.parser')
reviews = soup.select('.jJc9Ad') # 找到目前頁面所有評論的節點


reviews_len = 100 #要爬取的評論數
reviews_len_now = len(reviews)

# 滑頁到找到足夠的評論數
while reviews_len > reviews_len_now:
    driver.find_element(By.CLASS_NAME,'DxyBCb').send_keys(Keys.END)
    sleep_time = random.randint(15, 25)/10
    time.sleep(sleep_time)
    data = driver.page_source
    soup = BeautifulSoup(data,'html.parser')
    reviews = soup.select('.jJc9Ad')
    # reviews_len = reviews_len_now
    reviews_len_now = len(reviews)

print(reviews_len_now)
        
# 把評論和圖片點擊展開
buttons = driver.find_elements(By.CLASS_NAME,"w8nwRe")
for button in buttons:
    button.click()
more_pic = driver.find_elements(By.CLASS_NAME,"Tap5If")
for button in more_pic:
    button.click()


recommands = []
data = driver.page_source
soup = BeautifulSoup(data,'html.parser')
for i in range(len(reviews)):
    pic_urls =[]
    review = soup.select('.jJc9Ad')[i]
    user = review.select_one('.d4r55').text
    star = review.select_one('.DU9Pgb .kvMYJc').get('aria-label')
    time = review.select_one('.rsqaWe').text
    try:
        pics = review.select('.Tya61d')
        for pic in pics:
            pic_urls.append(pic.get('style').split('url("')[1].split('=')[0])
    except:
        pass
    content =review.select_one('.MyEned .wiI7pd').text
    recommands.append([user,time,star,content,pic_urls])

df = pd.DataFrame(recommands)
df.columns = ['user','time','star','recommand','pics']