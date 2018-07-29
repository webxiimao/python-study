import struct
from socket import *
import os


def main():
    downloadFileName = input("请输入要下载的文件名")
    upSocket = socket(AF_INET, SOCK_DGRAM)
    upSocket.bind(('',7788))
    requestFileData = struct.pack("!H%dsb5sb"%len(downloadFileName),1,downloadFileName.encode("utf-8"),0,b'octet',0)
    upSocket.sendto(requestFileData,('192.168.8.168',69))
    num = 0
    flag = True
    f = open(downloadFileName,'wb+')
    while True:
        responseData = upSocket.recvfrom(1024)
        recvData ,serverInfo = responseData
        opNum = struct.unpack("!H",recvData[:2])#获取的操作码
        packNum = struct.unpack('!H',recvData[2:4])#获取的数据包快编码
        if opNum[0] == 3:
            num = num + 1
            if num == 65536:
                num = 0
            if num == packNum[0]:
                f.write(recvData[4:])
                # num = packNum[0]
            ackData = struct.pack("!HH",4,packNum[0])
            upSocket.sendto(ackData,serverInfo)

        elif opNum[0] == 5:
            flag = False
            print("对不起没有这个文件")

        if len(recvData) < 516:
            break


    if flag == True:
        f.close()
    else:
        os.unlink(downloadFileName)


if __name__ == "__main__":
    main()