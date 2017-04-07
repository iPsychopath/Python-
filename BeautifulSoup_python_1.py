# -*- coding:utf-8 -*-
#   导入模块
import re

from bs4 import BeautifulSoup as bs

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
#   设置BeautifulSoup的解释器为html.parser
soup=bs(html_doc,'html.parser')

#   格式化输出
print(soup.prettify())

#   查找输出id为link2的标签的内容
print(soup.find(id='link2').string)

#   查找输出全部a标签的内容
for i in soup.find_all("a"):
    print(i.string)

#   查找输出p标签并且class未story标签的内容
print(soup.find("p",{"class":"story"}).getText())

#   查找A标签，并且使用正则匹配并赋给data
data=soup.findAll("a",href=re.compile(r"^http://example\.com/"))

#   查看data的长度
print(len(data))

#   循环输出data的href链接
for i in data:
    print(i["href"])
