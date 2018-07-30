from socket import *
from multiprocessing import Process
import re
import sys



WGET_PYTHON_DIR = "./wgetpython";

class HTTPServer(object):
    '''
    web服务器
    '''
    def __init__(self ,app):
        self.web_server_socket = socket(AF_INET, SOCK_STREAM)
        self.web_server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.app = app

    #启动服务
    def start(self):
        self.web_server_socket.listen(10)
        while True:
            client_socket, client_addr = self.web_server_socket.accept()
            # self.handle_server(client_socket, client_addr)
            print("-----------新客户端链接--------------")
            client_server = Process(target=self.handle_server, args=(client_socket, client_addr))
            client_server.start()

    #处理服务
    def handle_server(self, clientSocket, clientAddr):
        recvData = clientSocket.recv(1024)
        request_lines = recvData.splitlines()
        for request_line in request_lines:
            print(request_line)
        print("**********************")

        request_start_line = request_lines[0].decode("utf-8")
        file_name = re.match(r'\w+ +(/[^ ]*)',request_start_line).group(1)
        method = re.match(r'(\w+) +/[^ ]*',request_start_line).group(1)
        print(file_name, method)
        env = {
            "PATH_INFO": file_name,
            "METHOD": method
        }

        #请求体

        response_body = self.app(env, self.start_response)

        response = self.response_headers + "\r\n" + response_body
        clientSocket.send(bytes(response, "utf-8"))

        clientSocket.close()


    def start_response(self, status, headers):
        response_headers = "HTTP/1.1" + status +'\r\n'

        for header in headers:
            response_headers += "%s:%s"%header +"\r\n"

        self.response_headers = response_headers


    #监听端口号
    def bind(self, port):
        self.web_server_socket.bind(('', port))



if __name__ == "__main__":
    sys.path.insert(1, WGET_PYTHON_DIR)
    if len(sys.argv) < 2:
        sys.exit("python MyWebServer.py Module:app")
    # python MyWebServer.py  MyWebFrameWork:app
    module_name, app_name = sys.argv[1].split(":")
    # module_name = "MyWebFrameWork"
    # app_name = "app"
    m = __import__(module_name)
    app = getattr(m, app_name)
    http_server = HTTPServer(app)
    # http_server.set_port
    http_server.bind(8000)
    http_server.start()