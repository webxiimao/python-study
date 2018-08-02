from socket import *
import os


def main():

    host = "192.168.3.227"

    if os.name == "nt":
        sock_potocol = IPPROTO_IP
    else:
        sock_potocol = IPPROTO_ICMP


    s = socket(AF_INET, SOCK_RAW, sock_potocol)
    s.bind((host,0))
    while True:
        s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

        if os.name == "nt":
            s.ioctl(SIO_RCVALL, RCVALL_ON)

        print(s.recvfrom(65535))

        if os.name == "nt":
            s.ioctl(SIO_RCVALL, RCVALL_OFF)







if __name__ == "__main__":
    main()