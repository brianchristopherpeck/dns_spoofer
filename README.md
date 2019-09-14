### ONLY WORKS ON LINUX SYSTEMS!!!
#### For local testing 
##### Set this in Arp Spoofer DIR
Set up the Forward packet chain to be trapped in a Net Filter Queue and set the number of that Queue to 0
`iptables -I FORWARD -j NFQUEUE --queue-num 0`
To trap packets leaving Attacker CPU for local testing
`iptables -I OUTPUT -j NFQUEUE --queue-num 0`
To trap packets coming in Attacker CPU for local testing
`iptables -I INPUT -j NFQUEUE --queue-num 0`
Once done make sure you flush the iptables
`iptables --flush`

### Install netfilterqueue
pip install netfilterqueue

### Install scapy
pip install scapy

### Import netfilterqueue
`import netfilterqueue`

#### ToDo:
- Upgrade to Python3