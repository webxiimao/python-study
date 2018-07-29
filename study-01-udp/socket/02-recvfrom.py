from socket import *
upSocket = socket(AF_INET,SOCK_DGRAM)
upSocket.bind(('',7788))
recvData = upSocket.recvfrom(1024)
content ,destInfo = recvData
print("%s"%content.decode('gb2312'))


