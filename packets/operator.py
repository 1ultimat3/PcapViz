from util.decorators import packet_filter
from util.functions import combine_lists


def merger(packet_lists):
    return combine_lists(packet_lists)

@packet_filter
def exclude_ips(packets, ips):
    new_packet_list = []
    for packet in packets:
        if "IP" in packet:
            ip_layer = packet['IP']
            if not ip_layer.src in ips and ip_layer.dst not in ips:
                new_packet_list.append(packet)
        else:
            new_packet_list.append(packet)
    return new_packet_list


@packet_filter
def get_layer(packets, layer):
    all_packets = []
    for packet in packets:
        if layer in packet:
            all_packets.append(packet)
    return all_packets
