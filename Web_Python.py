# -*- coding: utf-8 -*-
import string
import re
import web
from urllib import request
import codecs

urls = (
    '/tra', 'Tra',
    '/atl', 'atl',
    '/news', 'news',
    '/id', 'maoyanid',
    '/maoyan', 'maoyan',
    '/api', 'api',
    '/index', 'blog',
    '/(.*)', 'hello'
)
app = web.application(urls, globals())


class Spider_movie(object):
    def __init__(self):
        self.cur_url = "http://maoyan.com/films/"
        self.datas = []
        self.imgs = []
        self._top_num = 1
        self._img_num = 1

    def get_page(self, id):
        url = self.cur_url + str(id)
        my_page = request.urlopen(url).read().decode("utf-8")
        self.find_content(my_page)

    def find_content(self, my_page):
        temp_data = []
        temp_img = []
        movie_items = re.findall(r'<div class="star-on" style="width:(.*?)%;"></div>', my_page)
        print(movie_items)
        movie_itemss = re.findall(r'<img class="default-img".*?src="(.*?)" alt="">', my_page)
        # print(movie_itemss)
        for index, item in enumerate(movie_items):
            if item.find(" ") == -1:
                temp_data.append(item)
                self._top_num += 1
        self.datas.extend(temp_data)
        self.imgs = movie_itemss


class Spider_news(object):
    def __init__(self):
        self.page = 1
        self.cur_url = "http://maoyan.com/news?showTab=2&offset={page}"
        self.datas = [[], [], [], []]

    def get_page(self, cur_page):
        # print(self.cur_url)
        url = self.cur_url.format(page=(cur_page - 1) * 10)
        # url = self.cur_url+str(id)
        # print(url)
        my_page = request.urlopen(url).read().decode("utf-8")
        return my_page

    def find_title(self, my_page):
        news_tittle = re.findall(r'<h4 class="news-header one-line">.*?}">(.*?)</a>.*?</h4>', my_page, re.S)
        news_img = re.findall(r'<a class="news-img".*?src="(.*?)".*?', my_page, re.S)
        news_text = re.findall(r'</h4>.*?<div class="latestNews-text">(.*?)</div>', my_page, re.S)
        news_count = re.findall(r'<span class="images-view-count view-count">(.*?)</span>', my_page, re.S)
        self.datas[0].extend(news_tittle)
        self.datas[1].extend(news_img)
        self.datas[2].extend(news_text)
        self.datas[3].extend(news_count)

    def start_spider(self):
        while self.page <= 3:
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1

class Spider_tra(object):
    def __init__(self):
        self.page = 1
        self.cur_url = "http://maoyan.com/news?showTab=3&offset={page}"
        self.datas = [[], [], []]

    def get_page(self, cur_page):
        url = self.cur_url.format(page=(cur_page - 1) * 10)
        my_page = request.urlopen(url).read().decode("utf-8")
        return my_page

    def find_title(self, my_page):
        news_img = re.findall(r'<img class="video-screenshot" src="(.*?)"', my_page, re.S)
        news_tittle = re.findall(r'<h4 class="video-name one-line">.*?>(.*?)</a>', my_page, re.S)
        news_count = re.findall(r'<span class="video-play-count">(.*?)</span>', my_page, re.S)
        self.datas[0].extend(news_tittle)
        self.datas[1].extend(news_img)
        self.datas[2].extend(news_count)

    def start_spider(self):
        while self.page <= 3:
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1

class Tra:
    def GET(self):
        my_spider = Spider_tra()
        my_spider.start_spider()
        json = '{'
        i = 0
        j = 0
        count = 1
        while i < len(my_spider.datas):
            while j < len(my_spider.datas[i]):
                json += '"' + str(count) + '":{'
                json += '"title": "' + my_spider.datas[i][j]
                json += '","img": "' + my_spider.datas[i + 1][j]
                json += '","count": "' + my_spider.datas[i + 2][j]
                json += '"},'
                j += 1
                count += 1
            i += 1
        json = json[:-1]
        json += '}'
        return json

class Spider_alt(object):
    def __init__(self):
        self.page = 1
        self.cur_url = "http://maoyan.com/news?showTab=4&offset={page}"
        self.datas = [[],[]]
        self.imgs = []
        # self.imgss = [[],[],[],[]]
        self._top_num = 1
        self._img_num = 1

    def get_page(self, cur_page):
        # print(self.cur_url)
        url = self.cur_url.format(page=(cur_page - 1) * 10)
        # url = self.cur_url+str(id)
        # print(url)
        my_page = request.urlopen(url).read().decode("utf-8")
        return my_page

    def find_title(self, my_page):
        alt_tittle = re.findall(r'<h4 class="images-header one-line">.*?data-act="images-click".*?>(.*?)</a>', my_page,re.S)
        alt_img = re.findall(r'data-act="images-click".*?<img src="(.*?)"',my_page, re.S)
        # print(len(alt_img))
        self.datas[0].extend(alt_tittle)
        self.datas[1].extend(alt_img)

    def start_spider(self):
        # self.cur_url=self.cur_url+str(id)
        # print(self.cur_url)
        while self.page <= 2:
            my_page = self.get_page(self.page)
            # print(self.get_page(self.page))
            self.find_title(my_page)
            self.page += 1


class atl:
    def GET(self):
        i=0
        j=1
        count=0
        json="{"
        my_spider = Spider_alt()
        my_spider.start_spider()
        # print(my_spider.datas[1][1])
        while i<len(my_spider.datas[0]):
            json += '"' + str(count) + '":{'
            json += '"title": "' + my_spider.datas[0][i]
            while j%3:
                # print(j)
                json += '","img' + str(j-1) + '": "' + my_spider.datas[1][j-1]
                j += 1
            json += '","img' + str(j - 1) + '": "' + my_spider.datas[1][j - 1]
            json += '"},'
            # print(i)
            i += 1
            j += 1
            count += 1
        json = json[:-1]
        json += '}'
        return json


class news:
    def GET(self):
        self.my_spider = Spider_news()
        self.my_spider.start_spider()
        self.json = '{'
        self.i = 0
        self.j = 0
        self.count = 1
        while self.i < len(self.my_spider.datas):
            # print(len(self.my_spider.datas[self.i]))
            while self.j < len(self.my_spider.datas[self.i]):
                self.json += '"' + str(self.count) + '":{'
                # print(self.my_spider.datas[2][2])
                self.json += '"title": "' + self.my_spider.datas[self.i][self.j]
                self.json += '","img": "' + self.my_spider.datas[self.i + 1][self.j]
                self.json += '","text": "' + self.my_spider.datas[self.i + 2][self.j]
                self.json += '","count": "' + self.my_spider.datas[self.i + 3][self.j]
                self.json += '"},'
                self.j += 1
                self.count += 1
            # print(self.i)
            self.i += 1
        self.json = self.json[:-1]
        self.json += '}'
        return self.json


class maoyanid:
    def GET(self):
        return open(u'id.html', 'r', -1, "utf-8").read()


class maoyan:
    def POST(self):
        data = web.input()
        if str(data.get("id")) == "None":
            self.id = "247875"
        else:
            self.id = data.get("id")
        self.i = 0
        my_spider = Spider_movie()
        my_spider.get_page(self.id)
        # print(my_spider.imgs[1])
        json = '{"grade":"' + ('%.1f' % (float(my_spider.datas[0]) * 0.1)) + '","Pro_grade":"' + (
        '%.1f' % (float(my_spider.datas[1]) * 0.1))
        # print(len(my_spider.imgs))
        if len(my_spider.imgs) > 0:
            json = json + '","img":{'
            while self.i < 5:
                json = json + '"img' + str(self.i) + '":"' + my_spider.imgs[self.i] + '",'
                self.i += 1
            json = json[:-1]
            json = json + '}}'
        return json


class api:
    def GET(self):
        with request.urlopen(
                'http://m.meilishuo.com/detail/mls/v1/h5?iid=1glxh9m&_ajax=1&cparam=MTQ4ODY0NzY5NF8xNXFjYWFzXzViZmI0N2I2ZmJjZDM3OWZhZDg3ZGIyMjRiZmFmYTFjXzE2XzBfMTcwODExNTE1XzIuMTYyOF8wXzFfMV8yMV8wXzA%3D') as f:
            data = f.read()
            # print('Status:', f.status, f.reason)
            # for k, v in f.getheaders():
            # print('%s: %s' % (k, v))
            return data.decode('utf-8')


class blog:
    def POST(self):
        data = web.input()
        # return data.get("user")
        # print(str(data.get("abc"))=="None")
        with request.urlopen(data.get("user")) as f:
            data = f.read()
            # print('Status:', f.status, f.reason)
            # for k, v in f.getheaders():
            # print('%s: %s' % (k, v))
            return data.decode('utf-8')


class hello:
    def GET(self, name):
        if not name:
            pass
            # name = 'World'
        # return 'Hello, ' + name + '!'
        # return open(u'1.html', 'r', -1, "utf-8").read()
        return 123


if __name__ == "__main__":
    app.run()
