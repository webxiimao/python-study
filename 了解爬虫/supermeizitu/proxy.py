import re
import requests
from bs4 import BeautifulSoup


def download_proxy():
    headers= {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    url = "http://www.66ip.cn/areaindex_19/1.html"
    html = requests.get(url,headers=headers)
    html_soup = BeautifulSoup(html.text, 'lxml')

    all_tr = html_soup.find_all('table')[2].find_all('tr')
    for tr in all_tr:
        ip_port = tr.find_all('td')[0].get_text() + ":" + tr.find_all('td')[1].get_text()
        print(ip_port.strip())


if __name__ == "__main__":
    download_proxy()