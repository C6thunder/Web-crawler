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


#热门
p = 10
k = 0
name = [] 
print("以下为热门")
for i in range(1,p+1):
    time.sleep(0.3)
    res = requests.get("https://www.gequbao.com/hot-music/"+str(i) , headers=headers)
    soup = BeautifulSoup(res.text,"html.parser").select("td a[class='text-info font-weight-bold']")
    for l in soup:
        name.append(re.search(r'">\s*\n*([^\n]*)\s*\n*<img',str(l)).group(1))
        print("="*10+f">{k}|"+name[k])
        k += 1




pg = 11
end = 20
while(1):


    song = name[pg]
    if pg == end:
        break

    # song = input("直接回车可退出\n歌名或索引[]:")
    # if song.isdigit():
    #     song = name[int(song)]
    # if not song:
    #     break

    time.sleep(0.2)
    res = requests.get("https://www.gequbao.com/s/"+song,headers=headers)
    soup = BeautifulSoup(res.text,"html.parser").select("div[class='col-8 col-content'] a[class='music-link d-block']")

    ty1 = r'href\s*=\s*"([^"]*)"'
    href = "https://www.gequbao.com" + re.search(ty1,str(soup)).group(1)

    print(href)


    #开始音频链接
    res = requests.get(href,headers=headers)
    soup = BeautifulSoup(res.text,"html.parser").select("script[type='text/javascript']")
    ty = r"window\.play_id\s*=\s*'([^']*)'"
    id = re.search(ty,str(soup[0])).group(1)

    print(f"解码post的id为{id}")


    datas = {
        "id": id
    }
    time.sleep(0.2)
    res1 = requests.post("https://www.gequbao.com/api/play-url",headers=headers,data=datas).json()["data"]["url"]
    print(f"《{song}》的链接为:\n {res1}")


    #判断可否下载
    time.sleep(0.3)
    headre = requests.head(res1, allow_redirects=True)
    content_length = headre.headers.get('Content-Length')
    print(f"{int(content_length)}字节")
    if int(content_length) < 500000:
        print("字节过小，可能不是目的歌曲")
        continue


    #下载歌曲
    response = requests.get(res1, stream=True)
    mp3_path = f"/home/thunder/音乐/{song}"+".mp3"
    os.makedirs(os.path.dirname(mp3_path), exist_ok=True)
    with open(mp3_path, 'wb') as f:
        f.write(response.content)
        print("成功下载")

    pg+=1





#总结：正则表达式真好用！！！