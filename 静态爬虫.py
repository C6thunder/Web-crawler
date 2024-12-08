from bs4 import BeautifulSoup
import requests
import time
import os
import re

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
}


#爬取闭区间
m ,n = (1,4)

#全部图库
tuku = "http://www.acgzyj.com/tuku_"

#只有二次元
meitu = "http://www.acgzyj.com/meitu_"

#只有coser
coser = "http://www.acgzyj.com/cosplay_"


out_url = []
for i in range(m,n+1):

    #选择爬取对象{tuku ，meitu ，coser}
    res = requests.get( meitu + str(i) + "/" ,headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    elements = soup.select("li[class='card sb'] a")


    #获取外层url
    for element in elements:

        out_url.append("http://www.acgzyj.com" + element["href"])


out_url = list(set(out_url))
print(out_url)
print("=="*40)


q = 1
for url in out_url:
            time.sleep(0.2)
            rep = requests.get(url=url,headers=headers)
            resoup = BeautifulSoup(rep.text, 'html.parser')        
            img = resoup.select("div[class='art-content'] img")

            k = 0
            for i in img:

                if not i.get('alt', None):
                    continue
                if not i.get('src', None):
                    continue


                alt = re.sub(r"\d","",i["alt"])


                if not os.path.exists('./ACG图片/'):
                    os.mkdir('./ACG图片/')
                if not os.path.exists('./ACG图片/' + alt ):
                    os.mkdir('./ACG图片/' + alt )


                imgurl = "http://www.acgzyj.com" + i["src"]


                if imgurl.lower().endswith('.jpg'): 
                    save_path = './ACG图片/' +alt + "/" + alt +str(k+1) + '.jpg'
                elif imgurl.lower().endswith('.jpeg'):
                    save_path = './ACG图片/' +alt + "/" + alt  +str(k+1) + '.jpeg'
                elif imgurl.lower().endswith('.bmp'):
                    save_path = './ACG图片/' +alt + "/" +  alt  +str(k+1) + '.bmp'       
                else:
                    save_path = './ACG图片/' +alt + "/" + alt  +str(k+1) + '.png'


                time.sleep(0.3)

                r = requests.get(imgurl,headers=headers,stream=True)
                
                if r.status_code == 200:
                    k+=1
                    with open(save_path,"wb") as f:
                        print("==> " + imgurl)
                        f.write(r.content)
                        print(alt +str(k+1))
                        print("=="*20+f"完成{q}张！"+"=="*20 +"\n")
                        q += 1







