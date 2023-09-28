# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 16:58:13 2023

@author: Leo
"""


url = "https://www.google.com/maps/place/%E9%87%91%E5%B3%B0%E9%AD%AF%E8%82%89%E9%A3%AF/@25.0320312,121.515924,17z/data=!3m1!5s0x3442a99eb5700fc7:0x4c531857fded6ce4!4m8!3m7!1s0x3442a99eb59cabfb:0xd9cf9cd1992ceb6c!8m2!3d25.0320264!4d121.5184989!9m1!1b1!16s%2Fg%2F1tj98pyk?hl=zh-TW&entry=ttu"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)
data = driver.page_source
soup = BeautifulSoup(data,'html.parser')
reviews = soup.select('.jJc9Ad')
reviews_len = 100
new_reviews_len = len(reviews)


# 滑頁到找到足夠的評論數
while reviews_len > new_reviews_len:
    driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]').send_keys(Keys.END)
    time.sleep(2)
    data = driver.page_source
    soup = BeautifulSoup(data,'html.parser')
    reviews = soup.select('.jJc9Ad')
    reviews_len = new_reviews_len
    new_reviews_len = len(reviews)
    if reviews_len == new_reviews_len:
        driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]').send_keys(Keys.END)
        time.sleep(2)
        data = driver.page_source
        soup = BeautifulSoup(data,'html.parser')
        reviews = soup.select('.jJc9Ad')
        reviews_len = new_reviews_len
        new_reviews_len = len(reviews)
print(new_reviews_len)
        

buttons = driver.find_elements(By.CLASS_NAME,"w8nwRe")
for button in buttons:
    button.click()
more_pic = driver.find_elements(By.CLASS_NAME,"Tap5If")
for button in more_pic:
    button.click()

recommands = []
data = driver.page_source
soup = BeautifulSoup(data,'html.parser')
df = pd.DataFrame()
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
    # print(i)

df = pd.DataFrame(recommands)
df.columns = ['user','time','star','recommand','pics']