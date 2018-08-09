import re
import requests
import random
from bs4 import BeautifulSoup
import time


class Download(object):


    def __init__(self):
        self.iplist = []  ##初始化一个list用来存放我们获取到的IP
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        url = "http://www.66ip.cn/areaindex_19/1.html"
        html = requests.get(url, headers=headers)
        html_soup = BeautifulSoup(html.text, 'lxml')
        all_tr = html_soup.find_all('table')[2].find_all('tr')
        iplist = []
        for tr in all_tr:
            ip_port = tr.find_all('td')[0].get_text() + ":" + tr.find_all('td')[1].get_text()
            iplist.append(ip_port.strip())
        self.iplist = iplist

        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def get(self, url, timeout, proxy=None, num_tries=6):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': UA ,'Referer':'http://www.mzitu.com/101553'}
        if proxy == None:
            try:
                return requests.get(url, headers=headers, timeout=timeout)
            except:
                if num_tries > 0:
                    print('num_tries:%s' % num_tries)
                    num = num_tries - 1
                    time.sleep(10)
                    print( '获取网页失败,10s后将获取倒数第' , num_tries  , '次尝试' )
                    return self.get(url, timeout, num_tries=num)
                else:
                    print('多次失败开始使用代理')
                    IP = str(random.choice(self.iplist).strip())
                    proxy = {'http':IP}
                    return self.get(url, timeout, proxy=proxy)
        else:
            try:
                IP = str(random.choice(self.iplist).strip())
                proxy = {'http':IP}
                return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            except:
                if num_tries > 0:

                    time.sleep(10)
                    IP = str(random.choice(self.iplist).strip())
                    proxy = {'http':IP}
                    print('正在更换代理倒数第', num_tries, '次尝试')
                    return self.get(url, timeout, proxy=proxy, num_tries = num_tries-1)
                else:
                    print('代理失效,取消代理')
                    return self.get(url, 3)



request = Download()

