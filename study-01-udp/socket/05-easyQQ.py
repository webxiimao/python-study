from socket import *
from threading import Thread


def recvData():
    while True:
        recvInfo = upSocket.recvfrom(1024)
        print("\r>>%s:%s"%(str(recvInfo[1]),recvInfo[0].decode('gb2312')))


def sendData():
    while True:
        sendInfo = input("\n<<")
        upSocket.sendto(sendInfo.encode("gb2312"),(connectIp,connectPort))


upSocket = None
connectIp = ""
connectPort = 0
def main():
    global upSocket
    global connectIp
    global connectPort

    upSocket = socket(AF_INET,SOCK_DGRAM)
    upSocket.bind(('',7788))
    connectIp = input("请输入连接方ip")
    connectPort = int(input('请输入连接放端口地址'))

    tr = Thread(target=recvData)
    ts = Thread(target=sendData)

    tr.start()
    ts.start()

    tr.join()
    ts.join()




if __name__ == "__main__":
    main()
