from socket import *
upSocket = socket(AF_INET,SOCK_DGRAM)
sendIp = input("请输入发送方ip")
sendPort = int(input("请输入发送方端口号"))
sendData = input("请输入发送内容")
upSocket.bind(("",7788))
upSocket.sendto(sendData.encode("utf-8"),(sendIp,sendPort))

