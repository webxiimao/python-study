from urllib.request import Request, urlopen
from urllib.parse import urlencode


class baidu_port(object):
    def __init__(self):
        self.url = "http://www.baidu.com/s"

    def search(self, keyword):
        word = { 'wd':keyword }
        search_word = urlencode(word)
        fullurl = self.url + '?' + search_word
        self.request(fullurl)

    def request(self, url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"'}
        request = Request(url, headers=headers)
        response = urlopen(request)

        print(response.read())






if __name__ == '__main__':
    keyword = input('请输入要查询的内容')
    request = baidu_port()
    request.search(keyword)
