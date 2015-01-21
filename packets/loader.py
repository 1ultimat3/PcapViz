from scapy.all import *
load_contrib("igmp")
load_contrib("igmpv3")


def get_packets(*files):
    return [rdpcap(_file) for _file in files]