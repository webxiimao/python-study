import os
from bs4 import BeautifulSoup
import requests


headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",'Referer':'http://www.mzitu.com/101553'}
all_url = "http://www.mzitu.com/all"
start_html =  requests.get(all_url,headers=headers)

# print(start_html.text)#直接获取了整个网页的html

Soup = BeautifulSoup(start_html.text, 'lxml')

all_a = Soup.find('div',class_='all').find_all('a')

for a in all_a:
    txt = a.get_text()
    path = str(txt).strip()
    os.makedirs(os.path.join('D:\mizitu1',path))
    # os.chdir('D:\mizitu\\'+path)
    os.chdir(os.path.join('D:\mizitu1',path))
    href = a['href']
    html = requests.get(href,headers=headers)
    html_soup = BeautifulSoup(html.text, 'lxml')


    # max_span = html_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
    if html_soup.find('div', class_='pagenavi') is None:
        pass
    else:
        max_span = html_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span)+1):
            url = href + "/" +str(page)
            img_html = requests.get(url,headers=headers)
            img_Soup = BeautifulSoup(img_html.text, 'lxml')
            img_url = img_Soup.find('div', class_='main-image').find('img')['src']
            name = img_url[-9:-4]
            img = requests.get(img_url,headers=headers)
            f = open(name+'.jpg','ab')
            f.write(img.content)
            f.close

