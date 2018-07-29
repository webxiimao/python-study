from socket import *

def main():
    upSocket = socket(AF_INET ,SOCK_DGRAM)
    upSocket.bind(('',7788))
    while True:
        recvData = upSocket.recvfrom(1024)
        print("%s:%s"%(str(recvData)[1],recvData[0].decode('gb2312')))

if __name__ == "__main__":
    main()