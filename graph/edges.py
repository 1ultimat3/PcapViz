from util.decorators import packet_filter
from scapy.all import Ether

@packet_filter
def generate_layer3_edges(packets):
    com_nodes = set()
    for packet in packets:
        if "IP" in packet:
            com_nodes.update([(packet["IP"].src, packet["IP"].dst)])
    return com_nodes

@packet_filter
def generate_layer2_edges(packets):
    com_nodes = set()
    for packet in packets:
        if packet.haslayer(Ether):
            try:
                com_nodes.update([(packet[Ether].src, packet[Ether].dst)])
            except IndexError:
                print "not added packet: %s" % str(packet.summary())
    return com_nodes
