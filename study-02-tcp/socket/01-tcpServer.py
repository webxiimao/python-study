from socket import *


def main():
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',8899))

    serverSocket.listen(5)
    while True:
        clientSocket ,clientInfo = serverSocket.accept()
        while True:
            recvData = clientSocket.recv(1024)
            print("%s:%s"%(clientInfo,recvData.decode("gb2312")))



if __name__ == "__main__":
    main()