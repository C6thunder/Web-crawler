from bs4 import BeautifulSoup
import requests
import time
import os
import re

'''
    首页：
    http://www.acgzyj.com/

    全部图库：
    http://www.acgzyj.com/tuku/

    coser：
    http://www.acgzyj.com/cosplay/

   
    分析：

    二次元角色：
    http://www.acgzyj.com/meitu/
    区别：2207，2206
    |-> http://www.acgzyj.com/meitu/2207.html
    |    |-> href="/meitu/2207.html"
    |
    |-> http://www.acgzyj.com/meitu/2206.html
    |    |-> href="/meitu/2206.html"
    总结：url = http://www.acgzyj.com/meitu/ + href

    
    1. 先获取外层url，例如：http://www.acgzyj.com/meitu/2207.html ，这种形式

'''



headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
}

res = requests.get('http://www.acgzyj.com/meitu', headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

# #mainbox > div.index-post > ul:nth-child(2) > li > a
elements = soup.select("li[class='card sb'] > a")
# 一个元素：<a href="/meitu/2173.html" target="_blank" title="碧蓝航线美图一轮游宅月季">
#       <div class="img sb"><img alt="碧蓝航线美图一轮游宅月季" class="lazyload img-cover" src="/static/upload/image/20241014/1728912392368716.jpg"/></div></a>
#  需要的是href="/meitu/2173.html"  -> 单个元素：element["href"]


out_url = []
for element in elements:
    out_url.append("http://www.acgzyj.com" + element["href"])       # 类似于 http://www.acgzyj.com/meitu/2173.html

# 去重，先转成set(不允许重复)，再转成list
out_url = list(set(out_url))

q = 1
k = 0
# 之后重复以上步骤，获取每个外层url的内层图片url
for url in out_url:
    time.sleep(0.2)
    rep = requests.get(url=url, headers=headers)
    resoup = BeautifulSoup(rep.text, 'html.parser')
    img = resoup.select("div.art-content img")       # 包含alt，src属性  
    for i in img:
        # 防止alt，src没有普遍性，导致报错
        if not i.get('alt', None):
            continue
        if not i.get('src', None):
            continue

        # 去除alt中的数字，在根据alt创建文件夹
        alt = re.sub(r"\d", "", i["alt"])
        if not os.path.exists('./ACG图片/'):
            os.mkdir('./ACG图片/')
        if not os.path.exists('./ACG图片/' + alt):
            os.mkdir('./ACG图片/' + alt)    # 例如：./ACG图片/碧蓝航线美图一轮游宅月季
        imgurl = "http://www.acgzyj.com" + i["src"]

        with open('./ACG图片/' + alt + "/" + str(k+1) + ".jpg","wb") as f:
            r = requests.get(imgurl, headers=headers)
            f.write(r.content)
            print(alt +str(k+1))
            print("=="*20+f"完成{q}张！"+"=="*20 +"\n")
            q += 1
            k += 1

'''
    本局mvp：marscode AI
    该代码仅供学习，不确定爬出的图片是否'正常'!
'''