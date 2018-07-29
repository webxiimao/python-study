from socket import *

def main():
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    udpSocket.sendto(b"haha",("192.168.8.168",8080))
    udpSocket.close()





if __name__ == "__main__":
    main()