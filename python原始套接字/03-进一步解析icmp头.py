from socket import *
from ctypes import *
import struct
import os


host = "192.168.3.227"

class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),  # 版本号
        ("version", c_ubyte, 4),  # 头长度
        ("tos", c_ubyte),  # 服务类型
        ("len", c_ushort),  # 总长
        ("id", c_ushort),  # 标识符
        ("offset", c_ushort),  # 标记
        ("ttl", c_ubyte),  # 生存时间
        ("protocol_num", c_ubyte),  # 协议类型
        ("sum", c_ushort),  # 头部效验
        ("src", c_ulong),  # 源ip
        ("dst", c_ulong)  # 目标ip
    ]


    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)


    def __init__(self, socket_buffer=None):
        protocol_map = {
            1:"ICMP",
            6:"TCP",
            17:"UDP"
        }

        self.protocol_src = inet_ntoa(struct.pack("<L",self.src))
        self.protocol_dst = inet_ntoa(struct.pack("<L",self.dst))

        try:
            self.protocol = protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)



class ICMP(Structure):

    _fields_ = [
        ("type", c_ubyte),#类型
        ("code", c_ubyte),#代码值
        ("checksum", c_ushort),#头部效验
        ("unused", c_ushort),#无用数据
        ("next_hop_mtu", c_ushort)#下一跳
    ]

    def __new__(self, sock_buffer):
        return self.from_buffer_copy(sock_buffer)

    def __init__(self, sock_buffer):
        pass




if os.name == "nt":
    socket_protocol = IPPROTO_IP
else:
    socket_protocol = IPPROTO_ICMP


s = socket(AF_INET, SOCK_RAW, socket_protocol)
s.setsockopt(IPPROTO_IP ,IP_HDRINCL, 1)
s.bind((host, 0))

if os.name == "nt":
    s.ioctl(SIO_RCVALL, RCVALL_ON)

try:
    while True:
        raw_buffer = s.recvfrom(65565)[0]
        protocol_header = IP(raw_buffer[0:20])
        print("Protocol: %s %s -> %s" % (protocol_header.protocol, protocol_header.protocol_src, protocol_header.protocol_dst))

        if protocol_header.protocol == "ICMP":
            offset = protocol_header.ihl * 4
            buf = raw_buffer[offset: offset + sizeof(ICMP)]
            icmp_header = ICMP(buf)
            print("ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code))

except KeyboardInterrupt:
# if we're on Windows turn off promiscuous mode
    if os.name == "nt":
        s.ioctl(SIO_RCVALL, RCVALL_OFF)




