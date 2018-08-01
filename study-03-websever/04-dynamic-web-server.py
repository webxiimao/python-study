from socket import *
from multiprocessing import Process
import re
import sys

WGSI_PYTHON_DIR = "./wsgipython"
HTTP_STATIC_DIR = "./html"

class HTTPServer(object):
    '''
    动态服务器
    '''
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def start(self):
        self.server_socket.listen(8)
        while True:
            client_server, client_addr = self.server_socket.accept()
            print("---------客户端:%s 已连接成功--------" % str(client_addr))
            handle_server_process = Process(target=self.handle_server, args=(client_server, client_addr))
            handle_server_process.start()
            client_server.close()

    def start_response(self, status, headers):
        '''
        根据wgsi协议定义start_response函数
        :param status:
        :param headers:
        :return:
        '''
        response_headers = "HTTP/1.1 "+status +'\r\n'
        for header in headers:
            response_headers += "%s:%s"%header + "\r\n"

        self.response_headers = response_headers


    def handle_server(self, client_server, client_addr):
        recvInfo = client_server.recv(1024)
        request_lines = recvInfo.splitlines()
        '''
        b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8899\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15\r\nAccept-Language: zh-cn\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n'      
        '''
        request_start_line = request_lines[0]
        file_name = re.match(r'\w+ +(/[^ ]*)',request_start_line.decode("utf-8")).group(1)
        method = re.match(r'(\w)+ +/[^ ]*',request_start_line.decode("utf-8")).group(1)

        if file_name.endswith(".py"):
            env = {
                "PATH_INFO":file_name,
                "METHOD":method
            }
            try:
                m = __import__(file_name[1:-3])
            except Exception:
                self.response_headers = "HTTP/1.1 404 ERROR\r\n"
                response_body = "not FOUND"
            else:
                response_body = m.application(env, self.start_response)

            response = self.response_headers + "\r\n" +response_body

        else:
            try:
                f = open(HTTP_STATIC_DIR + file_name, 'rb')
            except IOError:
                response_start_line = "HTTP/1.1 404 ERROR\r\n"
                response_header = "Server: MY SERVER\r\n"
                response_body = file_name+"IS NOT FOUND"
            else:
                file_data = f.read()
                f.close()
                response_start_line = "HTTP/1.1 200 OK\r\n"
                response_header = "Server: MY SERVER\r\n"
                response_body = file_data.decode("utf-8")

            response = response_start_line + response_header + "\r\n" + response_body
        client_server.send(bytes(response, "utf-8"))



    def bind(self, port):
        self.server_socket.bind(('', int(port)))


def main():
    sys.path.insert(1, WGSI_PYTHON_DIR)
    http_server = HTTPServer()
    http_server.bind(8899)
    http_server.start()

if __name__ == "__main__":
    main()