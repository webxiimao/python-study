from socket import *
upSocket = socket(AF_INET, SOCK_DGRAM)
upSocket.sendto(b"haah",("192.168.8.168",2233))