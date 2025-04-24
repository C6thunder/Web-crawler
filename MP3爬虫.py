from bs4 import BeautifulSoup
import requests
import time
import re
import os


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
}




# 热门歌曲
p = 3
k = 0
name = [] 
print("以下为热门")
for i in range(1,p+1):
    time.sleep(0.2)
    res = requests.get("https://www.gequbao.com/hot-music/"+str(i) , headers=headers)
    soup = BeautifulSoup(res.text,"html.parser").select("td a[class='text-info font-weight-bold']")
    for l in soup:
        name.append(re.search(r'">\s*\n*([^\n]*)\s*\n*<img',str(l)).group(1))
        print("="*10+f">{k}|"+name[k])
        k += 1


pg = 35
end = 50
while(1):


    song = input("\n直接回车可退出\n歌名(手)或索引[]:")

    if song.isdigit():
        song = name[int(song)]
    if not song:
        break


    time.sleep(0.3)
    res = requests.get("https://www.gequbao.com/s/"+song,headers=headers)
    sp = BeautifulSoup(res.text,"html.parser")


    soup = sp.select("div[class='col-8 col-content'] a[class='music-link d-block']")
    singername = sp.select("small[class='text-jade font-weight-bolder align-middle']")


    ty1 = r'href\s*=\s*"([^"]*)"'
    ty2 = r"<span>\s*([^>]*)\s*</span>"
    href = []
    find_ty1 = re.findall(ty1,str(soup))
    find_ty2 = re.findall(ty2,str(soup))
    o = 0
    for i in find_ty1:

        #打印同名不同歌曲及作者
        print("\n"+f"[{o}]"+">"*6 +f"({singername[o].get_text(strip=True)})" + find_ty2[o])

        hrefcache = "https://www.gequbao.com" + i
        href.append(hrefcache)

        #打印外层链接
        print(href[o],end="\n\n")
        o+=1 



    num = input("以上为所有搜索结果\n\n"+"选择编号(回车返回)[=>]:")
    if not num:
        continue


    #这里防止song在一开始输入的是人名，导致文件以人名来命名
    song = find_ty2[int(num)]
    href = href[int(num)]
    

    #开始音频链接
    # driver.get(href)    # 有时候不能用，就用requests进行请求
    response = requests.get(href,headers=headers)
    res = response.text
    # driver.quit()

    ty = r"window\.play_id\s*=\s*'([^']*)'"
    id = re.search(ty,res).group(1)  
    print(f"解码post的id为{id}")


    datas = {
        "id": id
    }


    time.sleep(0.3)
    res1 = requests.post("https://www.gequbao.com/api/play-url",headers=headers,data=datas).json()["data"]["url"]
    print(f"《{song}》的链接为:\n {res1}")


    #判断可否下载
    time.sleep(0.2)
    headre = requests.head(res1, allow_redirects=True)
    content_length = headre.headers.get('Content-Length')
    print(f"{int(content_length)}字节")

    pg+=1
    if int(content_length) < 500000:
        print("！！字节过小，可能不是目的歌曲！！")

    else:
        #下载歌曲
        response = requests.get(res1, stream=True)
        mp3_path = f"./{song}"+".mp3"
        os.makedirs(os.path.dirname(mp3_path), exist_ok=True)
        with open(mp3_path, 'wb') as f:
            f.write(response.content)
            print("成功下载")
            


