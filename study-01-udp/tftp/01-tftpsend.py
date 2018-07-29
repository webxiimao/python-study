import struct
from socket import *

upSocket = socket(AF_INET, SOCK_DGRAM)
upSocket.bind(('',7788))

def send_tftp_request():
    global upSocket
    fileName = "test.jpg"
    sendData = struct.pack("!H8sb5sb",1,fileName.encode('utf-8'),0,b"octet",0)
    # sendData = struct.pack("!H8sb5sb",1,b"test.jpg",0,b"octet",0)
    upSocket.sendto(sendData,('192.168.8.168',69))

    upSocket.close()


if __name__ == "__main__":
    send_tftp_request()