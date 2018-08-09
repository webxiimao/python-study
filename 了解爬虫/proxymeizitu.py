# import requests
from bs4 import BeautifulSoup
import os
from supermeizitu.download import request
from pymongo import MongoClient
import datetime


class Meizitu(object):
    def __init__(self):
        self.start_url = 'http://www.mzitu.com/all'
        client = MongoClient()
        db = client['meizixiezhenji']#创建一个库
        self.meizitu_collection = db['meizitu']#创建一个表
        self.title = ''  ##用来保存页面主题
        self.url = ''  ##用来保存页面地址
        self.img_urls = []  ##初始化一个 列表 用来保存图片地址



    def start(self):
        all_a = self.request(self.start_url).find('div',class_='all').find_all('a')
        for a in all_a:
            txt = a.get_text()
            self.title = txt
            if not self.makedir(txt):
                continue

            self.html(a)


    def html(self,a):
        href = a['href']
        self.url = href
        if self.meizitu_collection.find_one({'url':self.url}):
            print('该页面已被爬取过。。。')
        else:
            html_soup = self.request(href)
            if html_soup.find('div', class_='pagenavi') is None:
                pass
            else:
                max_span = html_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
                page_num = 0
                for page in range(1, int(max_span) + 1):
                    page_num += 1
                    url = href + "/" + str(page)
                    img_soup = self.request(url)
                    self.img_save(img_soup ,max_span, page_num)


    def img_save(self,url, max_span, page_num):
        url = url.find('div', class_='main-image').find('img')['src']
        self.img_urls.append(url)
        self.save(url, max_span, page_num)


    def save(self,img_url,max_span, page_num):
        name = img_url[-9:-4]
        img = self.request_img(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
        if int(max_span) == page_num:
            post = {
                'title':self.title,
                'url':self.url,
                'img_urls':self.img_urls,
                'datetime':datetime.datetime.now()
            }
            self.meizitu_collection.save(post)
            self.img_urls = []
            print('插入数据库成功')

    def request_img(self,url):
        html = request.get(url, 3)
        return html


    def request(self,url):
        html = request.get(url, 3)
        soup = BeautifulSoup(html.text, 'lxml')
        return soup


    def makedir(self, name):
        path = str(name).strip().replace(':','_') #去除空格
        # print(os.path.exists(os.path.join('D:\meizitu',path)))
        if not os.path.exists(os.path.join('D:\meizitu2',path)):
            print(u"新建文件夹----"+ path)
            os.makedirs(os.path.join('D:\meizitu2',path))
            os.chdir(os.path.join('D:\meizitu2',path))
            return True
        else:
            print(u'名字叫做'+ path + u'的文件夹已经存在了！')
            os.chdir(os.path.join('D:\meizitu2', path))
            return False





if __name__ == "__main__":
    meizitu = Meizitu()
    meizitu.start()
