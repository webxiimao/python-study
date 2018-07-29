from socket import *
from threading import Thread



def handleSocket(clientSocket,clientInfo):
    while True:
        recvData = clientSocket.recv(1024)

        if len(recvData)<=0:
            break
        else:
            print("%s:%s" % (str(clientInfo), recvData.decode('gb2312')))

        sendData = input("send:")
        clientSocket.send(sendData.encode("gb2312"))




def main():
    tcpSerSocket = socket(AF_INET,SOCK_STREAM)
    tcpSerSocket.bind(('',8899))
    tcpSerSocket.listen(5)
    while True:
        clientSocket, clientInfo = tcpSerSocket.accept()
        print('------11111------')
        t = Thread(target=handleSocket,args=(clientSocket,clientInfo))
        t.start()



if __name__ == "__main__":
    main()
