import time


HTML_TEMPLATE_DIR = "./html"

'''
模拟django 框架服务器
'''
class Application(object):
    def __init__(self, urls):
        self.urls = urls

    def __call__(self, env, start_response):
        path = env.get('PATH_INFO', '/')
        '''
        如果是静态资源 访问的是html
        '''
        if path.startswith('/static'):
            try:
                f= open(HTML_TEMPLATE_DIR + '/' + path[7:],'rb')

            except IOError:
                status = "404 NOT FOUND"
                headers = []
                start_response(status, headers)
                return "404 not found"
            else:
                html_data = f.read()
                f.close()
                status = "200 OK"
                headers = [
                    ('Content-Type', 'text/html')
                ]
                start_response(status, headers)
                return html_data.decode('utf-8')

        else:
            for url,application in self.urls:
                if path == url:
                    return application(env, start_response)


        status = "404 NOT FOUND"
        headers = []
        start_response(status, headers)
        return "404 not found"


def ctime(env, start_response):
    status = "200 OK"
    headers = []
    start_response(status, headers)
    return time.ctime()


def sayhello(env, start_response):
    status = "200 OK"
    headers = [
        ('Content-Type', 'text/plain')
    ]
    start_response(status, headers)
    return "hello boy!"


urls = [
    ('/ctime',ctime),
    ('/sayhello',sayhello)
]

app = Application(urls)
