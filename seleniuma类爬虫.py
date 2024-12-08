from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import requests
import os
import time

# wd = webdriver.Chrome()

#浏览器启动选项
option=webdriver.ChromeOptions()
#指定为无界面模式
option.add_argument('--headless')
# option.headless=True  #或者将上面的语句换成这条亦可
#创建Chrome驱动程序的实例
wd =webdriver.Chrome(options=option)




# 定义一个函数来模拟滚轮滚动
def scroll_to_bottom(driver):

    # JavaScript代码来滚动到页面底部

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



wd.get('https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=utf8&word=%E4%BA%8C%E6%AC%A1%E5%85%83%E5%9B%BE%E5%BA%93&fr=ala&ala=1&alatpl=normal&pos=0&dyTabStr=MCwzLDEsMiwxMyw3LDYsNSwxMiw5')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}


#网页滚动用来刷新图片
q=4
while(q):
    scroll_to_bottom(wd)
    sleep(1)
    q-=1




elements = WebDriverWait(wd, 20).until(

    EC.presence_of_all_elements_located((By.XPATH, "//img[@class='main_img img-hover']"))

)


 
i = 0
if not os.path.exists('./seleniuma爬虫图'):  #如果没有erciyuan则创建一个
    os.mkdir('./seleniuma爬虫图') 
for element in elements:
    t = element.get_attribute('src')
    if t.startswith("http"):
        i += 1
        path = f"./seleniuma爬虫图/二次元{i}.jpg"

        r = requests.get(t,headers=headers)
        r.raise_for_status()

        time.sleep(0.3)
        with open(path, 'wb') as f:
            f.write(r.content)
            f.close()

            print("**==================**")
            print(t)
            print(f'保存成功第{i}张图片')
            print("**^^^^^^^^^^^^^^^^^^**")
 
wd.quit()
