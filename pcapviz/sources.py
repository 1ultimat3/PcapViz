from scapy.utils import rdpcap
from itertools import chain


class ScapySource(object):

    @staticmethod
    def load(pcap_file_paths=[]):
        return list(chain(*[rdpcap(_file) for _file in pcap_file_paths]))

