from argparse import ArgumentParser
from packets.loader import get_packets
from packets.operator import *
from graph.edges import *
from graph.graphs import *
from graph.viz import *
from graph.stats import *

if __name__ == '__main__':

    parser = ArgumentParser(description='pcap topology drawer')
    parser.add_argument('-i', '--pcaps', nargs='*', help='capture files to be analyzed')
    parser.add_argument('-o', '--out', help='topology will be stored in the specified file')
    parser.add_argument('--layer2', action='store_true', help='create layer2 topology')
    parser.add_argument('--layer3', action='store_true', help='create layer3 topology')
    parser.add_argument('-e', '--exclude', nargs='*', help='exclude IPs from analysis')
    parser.add_argument('-f', '--frequent', action='store_true', help='print frequent nodes to stdout')
    args = parser.parse_args()

    if args.pcaps:
        packet_ls = merger(packet_lists=get_packets(*args.pcaps))
        if args.exclude:
            packet_ls = exclude_ips(packet_lists=packet_ls, ips=args.exclude)
        if args.layer2:
            edges = generate_layer2_edges(packet_lists=packet_ls)
        else:
            packet_ls = get_layer(packet_lists=packet_ls, layer="IP")
            edges = generate_layer3_edges(packet_lists=packet_ls)
        graphs = create_digraph(edge_lists=edges)

        if args.out:
            draw_edges(graphs=graphs, filename=args.out)

        if args.frequent:
            get_frequent_ips(graphs=graphs)