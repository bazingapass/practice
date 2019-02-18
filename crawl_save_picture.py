import requests
import re
from bs4 import BeautifulSoup
import os

url = "https://www.443zh.com/html/news/8363.html"
headers = {
    "User-Agent": "Mozilla/5.0",
}
resp = requests.get(url=url, headers=headers)
html = resp.content.decode()

soup = BeautifulSoup(html, features="html.parser")
img_list = soup.find_all('img')
for img in img_list:
    url = img["src"]
    # https://img.997pp.com/tp/2018/09/ck4bt3xyk0q.jpg
    # /2018/09/ck4bt3xyk0q.jpg
    full_path = re.match("^https://img.997pp.com/tp(.+)", url).group(1)
    # 分组分别获取路径和文件名
    file_dir = re.match(r"(/\d+/\d+/)(.+)", full_path).group(1)
    file_name = re.match(r"(/\d+/\d+/)(.+)", full_path).group(2)
    resp = requests.get(url=url, headers=headers)
    b_img = resp.content
    try:
        os.makedirs("." + file_dir)
    except FileExistsError:
        pass
    with open("." + file_dir + file_name, "bw") as f:
        f.write(b_img)

