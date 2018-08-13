from bs4 import BeautifulSoup
from supermeizitu.download import request
from mongodb_queue import MongoQueue




spider_queue = MongoQueue('meizixiezhenji', 'crawl_queue')
def start(url):
    '''
    把写真集所有的url 和标题插入数据库中
    :param url:
    :return:
    '''
    response = request.get(url, 3)
    soup = BeautifulSoup(response.text, 'lxml')
    all_a = soup.find('div',class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        url_a = a['href']
        spider_queue.push(url_a, title)


if __name__ == '__main__':
    start('http://www.mzitu.com/all')


