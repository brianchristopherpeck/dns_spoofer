#!/usr/bin/env python
import netfilterqueue

def process_packet(packet):
    # Prints packet payload
    print(packet.get_payload)
    # Drops the packet... cuts connection of target client
    packet.drop()
    # Intercept incoming packets and accept them instead of dropping them
    # packet.accept

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()