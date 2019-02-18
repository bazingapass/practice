from bs4 import BeautifulSoup
import requests
from time import sleep
import pymysql

url = "http://search.dangdang.com/?key=python&act=input&show=big&show_shop=0&page_index="

page_index = 1
book_list = []
while page_index <= 2:

    resp = requests.get(url+str(page_index))
    # 响应html
    html_doc = resp.text
    # 获得BeautifulSoup对象
    soup = BeautifulSoup(html_doc, features="html.parser")
    # 获得Tag对象(a标签列表[<a..>, <a..>, ])
    book_list += soup.find_all("a", {"class": "pic"})
    sleep(1)
    page_index += 1

connection = pymysql.connect(
    host="192.168.2.111",
    user="root",
    password="toor",
    db="crawl"
)

try:
    with connection.cursor() as cursor:
        for book in book_list:
            # 取出书籍名称并用引号包围
            book_title = '"' + book["title"] + '"'
            book_url = '"' + book["href"] + '"'
            sql = "insert into `books` (book_name, url) value ({}, {})"
            cursor.execute(sql.format(book_title, book_url))
finally:
    connection.close()
