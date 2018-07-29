from socket import *
from multiprocessing import Process
import re


STATIC_FILE_DIR = './html'
def server(clientSocket, clientInfo):

    recvData = clientSocket.recv(1024)
    print(recvData)
    '''
    b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8899\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15\r\nAccept-Language: zh-cn\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n'      
    '''
    request_lines = recvData.splitlines()

    for request_line in request_lines:
        print(request_line)

    request_start_line = request_lines[0]
    file_name = re.match(r'\w+ +(/[^ ]*)',request_start_line.decode('utf-8')).group(1)
    print(file_name)
    try:
        file = open(STATIC_FILE_DIR + file_name,'rb')
    except IOError:
        response_start_line = "HTTP/1.1 404 ERROR\r\n"
        response_headers = "Server: my Server\r\n"
        response_body = "file is not found"
    else:
        file_data = file.read()
        file.close()

        response_start_line = "HTTP/1.1 200 OK\r\n"
        response_headers = "Server: my Server\r\n"
        response_body = file_data.decode("utf-8")

        
    response = response_start_line + response_headers + "\r\n" + response_body

    clientSocket.send(bytes(response ,"utf-8"))
    clientSocket.close()



def main():
    tcpSerSocket = socket(AF_INET,SOCK_STREAM)
    # tcpSerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR ,1)
    tcpSerSocket.bind(('',8899))
    tcpSerSocket.listen(5)

    while True:
        clientSocket, clientInfo = tcpSerSocket.accept()

        p = Process(target=server, args=(clientSocket,clientInfo))
        p.start()
        clientSocket.close()




if __name__ == "__main__":
    main()
