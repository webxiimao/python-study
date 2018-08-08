# import requests
from bs4 import BeautifulSoup
import os
from supermeizitu.download import request


class Meizitu(object):
    def __init__(self):
        self.start_url = 'http://www.mzitu.com/all'
        # self.headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",'Referer':'http://www.mzitu.com/101553'}


    def start(self):
        all_a = self.request(self.start_url).find('div',class_='all').find_all('a')
        for a in all_a:
            txt = a.get_text()
            if not self.makedir(txt):
                continue

            self.html(a)


    def html(self,a):
        href = a['href']
        html_soup = self.request(href)

        if html_soup.find('div', class_='pagenavi') is None:
            pass
        else:
            max_span = html_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
            for page in range(1, int(max_span) + 1):
                url = href + "/" + str(page)
                img_soup = self.request(url)
                self.img_save(img_soup)


    def img_save(self,url):
        url = url.find('div', class_='main-image').find('img')['src']
        self.save(url)


    def save(self,img_url):
        name = img_url[-9:-4]
        img = self.request_img(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()


    def request_img(self,url):
        html = request.get(url, 3)
        return html


    def request(self,url):
        html = request.get(url, 3)
        soup = BeautifulSoup(html.text, 'lxml')
        return soup


    def makedir(self, name):
        path = str(name).strip()#去除空格
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
