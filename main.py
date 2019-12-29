from argparse import ArgumentParser

from pcapviz.core import GraphManager
from pcapviz.sources import ScapySource

# make this global so we can use it for tests

parser = ArgumentParser(description='pcap topology and message mapper')
parser.add_argument('-i', '--pcaps', nargs='*', default='test/test.pcap',help='space delimited list of capture files to be analyzed')
parser.add_argument('-o', '--out', help='topology will be stored in the specified file')
parser.add_argument('-g', '--graphviz', help='graph will be exported to the specified file (dot format)')
parser.add_argument('--layer2', action='store_true', help='create layer2 topology')
parser.add_argument('--layer3', action='store_true', help='create layer3 topology - 3 is the default')
parser.add_argument('--layer4', action='store_true', help='create layer4 topology')
#parser.add_argument('-e', '--exclude', nargs='*', help='exclude nodes from analysis')
parser.add_argument('-fi', '--frequent-in', action='store_true', help='print frequently contacted nodes to stdout')
parser.add_argument('-fo', '--frequent-out', action='store_true', help='print frequent source nodes to stdout')
parser.add_argument('-G', '--geopath', default='/usr/share/GeoIP/GeoLite2-City.mmdb', help='path to maxmind geodb data')
parser.add_argument('-l', '--geolang', default='en', help='Language to use for geoIP names')
parser.add_argument('-E', '--layoutengine', default='sfdp', help='Graph layout method - dot, sfdp etc.')
parser.add_argument('-s', '--shape', default='diamond', help='Graphviz node shape - circle, diamond, box etc.')
args = parser.parse_args()

if __name__ == '__main__':
    if args.pcaps:
        packets = ScapySource.load(args.pcaps)

        #if args.exclude:
        #    packet_ls = exclude_ips(packet_lists=packet_ls, ips=args.exclude)
        layer = 3
        if args.layer2:
            layer = 2
        elif args.layer4:
            layer = 4

        g = GraphManager(packets, layer=layer, args=args)

        if args.out:
            g.draw(filename=args.out)

        if args.frequent_in:
            g.get_in_degree()

        if args.frequent_out:
            g.get_out_degree()

        if args.graphviz:
            g.get_graphviz_format(args.graphviz)
