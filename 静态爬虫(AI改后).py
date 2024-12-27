from bs4 import BeautifulSoup
import requests
import random
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
m, n = 1, 4

#选择爬取对象{tuku ，meitu ，coser}
base_url = "http://www.acgzyj.com/meitu_"

def fetch_page(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_image(img_url, save_path):
    try:
        response = requests.get(img_url, headers=headers, stream=True)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    except requests.RequestException as e:
        print(f"Error saving {img_url}: {e}")
        return False

out_url = []
for i in range(m, n + 1):
    res = fetch_page(base_url + str(i) + "/")
    if res is None:
        continue

    soup = BeautifulSoup(res.text, 'html.parser')
    elements = soup.select("li[class='card sb'] a")

    for element in elements:
        out_url.append("http://www.acgzyj.com" + element["href"])

out_url = list(set(out_url))


# Write out_url to a log file
def write_log(string):
    with open('ACG.log', 'a') as log_file:
        log_file.write(string)

write_log("以下为日志文件："+ '\n')
h = 0
for url in out_url:
    h+=1
    if h%2!=0 or h==1:
        write_log(url+'\t')
    else:
        write_log(url+'\n')
print("已生成日志文件！")

q = 1
for url in out_url:
    time.sleep(round(random.randint(1, 6) * 0.1, 1))
    rep = fetch_page(url)
    if rep is None:
        continue

    resoup = BeautifulSoup(rep.text, 'html.parser')
    img_elements = resoup.select("div[class='art-content'] img")

    for k, img in enumerate(img_elements):
        if not img.get('alt') or not img.get('src'):
            alt = "0"
            continue

        alt = re.sub(r"\d", "", img["alt"])
        img_dir = os.path.join('./ACG图片', alt)
        os.makedirs(img_dir, exist_ok=True)

        img_url = "http://www.acgzyj.com" + img["src"]
        ext = os.path.splitext(img_url)[1].lower()
        save_path = os.path.join(img_dir, f"{alt}{k + 1}{ext}")

        time.sleep(round(random.randint(1, 6) * 0.1, 1))
        if save_image(img_url, save_path):
            print(f"==> {img_url}")
            print(f"{alt}{k + 1}")
            print("==" * 20 + f"完成{q}张！" + "==" * 20 + "\n")
            q += 1
    if alt !="0" :
        write_log("\n"+alt +"文件夹已完成" + ":" + url)


