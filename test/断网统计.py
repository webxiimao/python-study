import requests
from pymongo import MongoClient, DESCENDING
import random
import time


class network_status(object):
    '''
    对家庭网络断网次数和时间进行统计
    '''
    def __init__(self):
        self.url = "https://www.baidu.com"
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
        client = MongoClient()
        db = client['network']

        self.net_collection = db['network_status']

        results = self.net_collection.find().sort('time', DESCENDING).limit(1)
        self.count = int([result['time'] for result in results][0]) + 1
        self.status = 200
        self.begin_time = None
        self.end_time = None

    '''
    启动服务
    '''
    def start(self):

        while True:
            time.sleep(5)
            ua = random.choice(self.user_agent_list)
            headers = {'User-Agent': ua}
            try:
                response = requests.get(self.url, headers=headers)
                if self.status == 500:
                    self.end_time = time.time()
                    cut_time = self.end_time - self.begin_time
                    print('网络中断开始时间:',self.time_format(self.begin_time))
                    print('网络中断结束时间:',self.time_format(self.end_time))
                    print('网络连接恢复,中断时间为:',round(cut_time,2),'s')
                    post = {
                        'time':self.count ,
                        'begin_time':self.time_format(self.begin_time),
                        'end_time':self.time_format(self.end_time),
                        'break_time':round(cut_time,2)
                    }
                    self.net_collection.save(post)

                    self.reset_params()
                else:
                    print(response.status_code)
            except:
                if self.status is not 500:
                    self.status = 500
                    self.begin_time = time.time()
                    print('网络连接中断第', self.count, '次')

    def reset_params(self):
        '''
        复位指针数据
        :return:
        '''
        self.end_time = None
        self.begin_time = None
        self.count += 1
        self.status = 200

    def time_format(self, times):
        '''
        日期格式化
        :param times: 时间戳
        :return: 标准时间格式
        '''
        now = int(times)
        t = time.localtime(now)
        return time.strftime("%Y-%m-%d %H:%M:%S", t)

if __name__ == '__main__':
    net = network_status()
    net.start()