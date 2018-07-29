from socket import *
from multiprocessing import Process


def server(clientSocket, clientInfo):

    recvData = clientSocket.recv(1024)
    print(recvData)
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: my Server\r\n"
    response_body = "hello,world!"
    response = response_start_line + response_headers + "\r\n" + response_body

    clientSocket.send(bytes(response ,"utf-8"))
    clientSocket.close()



def main():
    tcpSerSocket = socket(AF_INET,SOCK_STREAM)
    tcpSerSocket.bind(('',8899))
    tcpSerSocket.listen(5)

    while True:
        clientSocket, clientInfo = tcpSerSocket.accept()

        p = Process(target=server, args=(clientSocket,clientInfo))
        p.start()
        clientSocket.close()




if __name__ == "__main__":
    main()