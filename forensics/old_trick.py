from scapy.all import *
import base64

capture = rdpcap('older_trick.pcap')
ping_data = ""

pings = [p for p in capture if ICMP in p]

for packet in pings:
    if packet[ICMP].type == 8: # Echo request
        ping_data += packet.load

print(base64.b64decode(ping_data))