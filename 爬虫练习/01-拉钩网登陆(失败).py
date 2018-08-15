import requests
from bs4 import BeautifulSoup
import hashlib

def lagou_spider():
    url = 'https://passport.lagou.com/login/login.json'
    sess = requests.Session()
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

    orgin_pass = "myy436627"
    hl1 = hashlib.md5()
    hl2 = hashlib.md5()
    hl1.update(orgin_pass.encode(encoding='utf-8'))
    md5_pass = hl1.hexdigest()

    second_pass = "veenike" + md5_pass + "veenike"

    hl2.update(second_pass.encode(encoding='utf-8'))
    password = hl2.hexdigest()
    print(password)


    data = {
        'isValidate':True,
        'username':13168733941,
        'request_form_verifyCode':None,
        'submit':None,
        'password':password
    }

    proxies = {
        'http':'127.0.0.1:8888'
    }

    responseCookie = sess.post(url,data=data,proxies=proxies,headers=headers)
    # response = sess.get('https://account.lagou.com/v2/account/userinfo.html',headers=headers)
    print(responseCookie.text)








if __name__ == '__main__':
    lagou_spider()