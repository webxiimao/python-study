from supermeizitu.download import request
from bs4 import BeautifulSoup
from mongodb_queue import MongoQueue
from threading import Thread
import multiprocessing
import time
import os



def thread_crawler( max_threading=10, sleep_time=1):
    crawl_queue = MongoQueue('meizixiezhenji', 'crawl_queue')##获取的所有url 的队列
    img_queue = MongoQueue('meizixiezhenji', 'img_queue')##url的实际队列

    def pageurl_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                print('从队列中抽取',url)
            except KeyError:
                print('队列没有数据')
                break
            else:
                img_urls = []
                req = request.get(url ,3).text
                title = crawl_queue.pop_title(url)
                path = str(title).replace('?', '').replace(':','') ##测试过程中发现一个标题有问号
                makedir(path)
                max_span = BeautifulSoup(req, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1, int(max_span) + 1):
                    page_url = url + '/' + str(page)
                    img_url = BeautifulSoup(request.get(page_url, 3).text, 'lxml').find('div', class_='main-image').find('img')['src']
                    img_urls.append(img_url)
                    save(img_url)
                img_queue.push_imgurl(title, img_urls)
                print('插入数据库成功')


    def save(img_url):
        name = img_url[-9:-4]
        print(u'开始保存：', img_url)
        img = request.get(img_url, 3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def makedir(name):
        path = str(name).strip().replace(':', '_').replace('?', '_')  # 去除空格
        # print(os.path.exists(os.path.join('D:\meizitu',path)))
        if not os.path.exists(os.path.join('D:\meizitu2', path)):
            print(u"新建文件夹----" + path)
            os.makedirs(os.path.join('D:\meizitu2', path))
            os.chdir(os.path.join('D:\meizitu2', path))
            return True
        else:
            print(u'名字叫做' + path + u'的文件夹已经存在了！')
            os.chdir(os.path.join('D:\meizitu2', path))
            return False


    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) <  max_threading or crawl_queue.peek():
            thread = Thread(target=pageurl_crawler)
            # thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        time.sleep(sleep_time)


def process_crawler():
    process = []
    # num_process = multiprocessing.cpu_count()
    num_process = 2
    print('将为你启动进程数为',num_process)
    for i in range(num_process):
        p = multiprocessing.Process(target=thread_crawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()






if __name__ == '__main__':
    process_crawler()