from argparse import ArgumentParser

from pcapviz.core import GraphManager
from pcapviz.sources import ScapySource
from scapy.all import *
from scapy.layers.http import HTTP


# make this global so we can use it for tests

parser = ArgumentParser(description='pcap topology and message mapper')
parser.add_argument('-i', '--pcaps', nargs='*', default='test/test.pcap',help='space delimited list of capture files to be analyzed')
parser.add_argument('-o', '--out', help='topology will be stored in the specified file')
parser.add_argument('-g', '--graphviz', help='graph will be exported to the specified file (dot format)')
parser.add_argument('--layer2', action='store_true', help='device topology network graph')
parser.add_argument('--layer3', action='store_true', help='ip message graph. Default')
parser.add_argument('--layer4', action='store_true', help='tcp/udp message graph')
parser.add_argument('-d','--DEBUG', action='store_true', help='show debug messages')
parser.add_argument('-w', '--whitelist', nargs='*', help='Whitelist of protocols - only packets matching these layers shown')
parser.add_argument('-b', '--blacklist', nargs='*', help='Blacklist of protocols - NONE of the packets having these layers shown')
parser.add_argument('-fi', '--frequent-in', action='store_true', help='print frequently contacted nodes to stdout')
parser.add_argument('-fo', '--frequent-out', action='store_true', help='print frequent source nodes to stdout')
parser.add_argument('-G', '--geopath', default='/usr/share/GeoIP/GeoLite2-City.mmdb', help='path to maxmind geodb data')
parser.add_argument('-l', '--geolang', default='en', help='Language to use for geoIP names')
parser.add_argument('-E', '--layoutengine', default='sfdp', help='Graph layout method - dot, sfdp etc.')
parser.add_argument('-s', '--shape', default='diamond', help='Graphviz node shape - circle, diamond, box etc.')
parser.add_argument('-n', '--nmax', default=100, help='Automagically draw individual protocols where useful if more than --nmax nodes. 100 seems too many for any one graph.')

args = parser.parse_args()

llook = {'DNS':DNS,'UDP':UDP,'ARP':ARP,'NTP':NTP,'IP':IP,'TCP':TCP,'Raw':Raw,'HTTP':HTTP,'RIP':RIP,'RTP':RTP}

if __name__ == '__main__':
	if args.pcaps:
		bl=[]
		wl=[]
		pin = ScapySource.load(args.pcaps)
		if args.whitelist != None and args.blacklist != None:
			print('### Parameter error: Specify --blacklist or specify --whitelist but not both together please.')
			sys.exit(1)
		packets = pin
		if args.whitelist: # packets are returned from ScapySource.load as a list so cannot use pcap.filter(lambda...)
			wl = [llook[x] for x in args.whitelist]
			packets = [x for x in pin if sum([x.haslayer(y) for y in wl]) > 0 and x != None]  
		elif args.blacklist:
			bl = [llook[x] for x in args.blacklist]
			packets = [x for x in pin if sum([x.haslayer(y) for y in bl]) == 0 and x != None]  
		if args.DEBUG and (args.blacklist or args.whitelist):
			print('### Read', len(pin), 'packets. After applying supplied filters,',len(packets),'are left. wl=',wl,'bl=',bl)
		layer = 3
		if args.layer2:
			layer = 2
		elif args.layer4:
			layer = 4
		args.nmax = int(args.nmax)
		g = GraphManager(packets, layer=layer, args=args)
		nn = len(g.graph.nodes())
		if nn > args.nmax:
			print('Asked to draw %d nodes with --nmax set to %d. Will also do useful protocols separately' % (nn,args.nmax))
			for kind in llook.keys():
				subset = [x for x in packets if x.haslayer(kind) and x != None]  
				if len(subset) > 2:
					sg = GraphManager(subset,layer=layer, args=args)
					nn = len(sg.graph.nodes())
					if nn > 2:
						ofn = '%s_%d_%s' % (kind,nn,args.out)
						sg.draw(filename = ofn)
						print('drew %s %d nodes' % (ofn,nn))
		if args.out:
			g.draw(filename=args.out)

		if args.frequent_in:
			g.get_in_degree()

		if args.frequent_out:
			g.get_out_degree()

		if args.graphviz:
			g.get_graphviz_format(args.graphviz)
