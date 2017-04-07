#   导入模块    设置编码
# -*- coding:utf-8 -*-
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import MySQLdb

#   配置连接MySQL
config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'root',
          'db':'wikiurl',
          'charset':'utf8',
          }
#   打开维基百科url，设置编码
resp = urlopen("https://en.wikipedia.org/wiki/Main_Page").read().decode("utf-8")
#   设置BeautifulSoup的解释器为html.parser
soup = BeautifulSoup(resp,"html.parser")
#   获取所有A标签开头为/wiki/的连接
listurls=soup.find_all("a",href=re.compile("^/wiki/"))

for url in listurls:
    #   判断连接不为jpg,png结尾
    if not re.search("\.(jpg|png|JPG|PNG)$",url["href"]):
        # len(url)
        #   把得到的连接加上https://en.wikipedia.org拼接成完全的URL
        url_url="https://en.wikipedia.org"+url["href"]
        #   输出查看是否正确
        # print(url.getText(),"<------>","https://en.wikipedia.org"+url["href"])
        #   连接数据库
        conn = MySQLdb.connect(**config)
        #   获取对象
        cursor = conn.cursor()
        try:
            #   SQL插入语句
            sql="insert into `wiki_url`(`url_id`,`url_name`,`url_url`) VALUES(null,%s,%s)"
            #   执行SQL语句
            cursor.execute(sql,(url.getText(),url_url))
            #   全部执行成功后执行提交事务
            conn.commit()
        except Exception as e:
            #   执行错误后执行回滚事务
            conn.rollback()
        finally:
            #关闭资源
            cursor.close()
            conn.close()

