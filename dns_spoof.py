#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    # Prints packet payload
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.hasLayer(scapy.DNSRR):
        print(scapy_packet.show())
    # Drops the packet... cuts connection of target client
    # packet.drop()
    # Intercept incoming packets and accept them instead of dropping them
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()