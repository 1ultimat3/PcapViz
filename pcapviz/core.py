from collections import OrderedDict

import networkx
import itertools
from networkx import DiGraph

from scapy.layers.inet import TCP, IP, UDP
import logging

import os
import socket
import maxminddb

"""
ross lazarus december 2019 forked from mateuszk87/PcapViz
changed geoIP lookup to use maxminddb
added reverse DNS lookup and cache
"""



class GraphManager(object):
	""" Generates and processes the graph based on packets
	"""

	def __init__(self, packets, layer=3, args=None):
		self.graph = DiGraph()
		self.layer = layer
		self.geo_ip = None
		self.args = args
		self.data = {}
		self.deeNS = {} # cache for reverse lookups
		try:
			self.geo_ip = maxminddb.open_database(self.args.geopath) # command line -G
		except:
			logging.warning("could not load GeoIP data from supplied parameter geopath %s" % self.args.geopath)

		if self.layer == 2:
			edges = map(self._layer_2_edge, packets)
		elif self.layer == 3:
			edges = map(self._layer_3_edge, packets)
		elif self.layer == 4:
			edges = map(self._layer_4_edge, packets)
		else:
			raise ValueError("Other layers than 2,3 and 4 are not supported yet!")

		for src, dst, packet in filter(lambda x: not (x is None), edges):
			if src in self.graph and dst in self.graph[src]:
				self.graph[src][dst]['packets'].append(packet)
			else:
				self.graph.add_edge(src, dst)
				self.graph[src][dst]['packets'] = [packet]

		for node in self.graph.nodes():
			self._retrieve_node_info(node)

		for src, dst in self.graph.edges():
			self._retrieve_edge_info(src, dst)

	def lookup(self,ip):
		"""deens caches all slow! fqdn reverse dns lookups from ip"""
		kname = self.deeNS.get(ip,None)
		if kname == None:
			kname = socket.getfqdn(ip) # PIA dns is slow!!
			self.deeNS[ip] = kname
		return (kname)


	def get_in_degree(self, print_stdout=True):
		unsorted_degrees = self.graph.in_degree()
		return self._sorted_results(unsorted_degrees, print_stdout)

	def get_out_degree(self, print_stdout=True):
		unsorted_degrees = self.graph.out_degree()
		return self._sorted_results(unsorted_degrees, print_stdout)

	def _sorted_results(self,unsorted_degrees, print_stdout):
		sorted_degrees = OrderedDict(sorted(list(unsorted_degrees), key=lambda t: t[1], reverse=True))
		for i in sorted_degrees:
			if print_stdout:
				nn = self.lookup(i)
				if (nn == i):
					print(sorted_degrees[i], i)
				else:
					print(sorted_degrees[i],i,nn)
		return sorted_degrees

	def _retrieve_node_info(self, node):
		self.data[node] = {}
		city = None
		country = None
		if self.layer >= 3 and self.geo_ip:
			if self.layer == 3:
				self.data[node]['ip'] = node
			elif self.layer == 4:
				self.data[node]['ip'] = node.split(':')[0]
			node_ip = self.data[node]['ip']
			try:
				mmdbrec = self.geo_ip.get(node_ip)
				if mmdbrec != None:
					countryrec = mmdbrec.get('city',None)
					cityrec = mmdbrec.get('country',None)
					if countryrec: # some records have one but not the other....
						country = countryrec['names'].get(self.args.geolang,None)
					if cityrec:
						city =  cityrec['names'].get(self.args.geolang,None)
				self.data[node]['country'] = country if country else 'private'
				self.data[node]['city'] = city if city else 'private'
			except:
				# no lookup so not much data available
				del self.data[node]
				
		#TODO layer 2 info?


	def _retrieve_edge_info(self, src, dst):
		edge = self.graph[src][dst]
		if edge:
			packets = edge['packets']
			edge['layers'] = set(list(itertools.chain(*[set(GraphManager.get_layers(p)) for p in packets])))
			edge['transmitted'] = sum(len(p) for p in packets)
			edge['connections'] = len(packets)

	@staticmethod
	def get_layers(packet):
		return list(GraphManager.expand(packet))

	@staticmethod
	def expand(x):
		yield x.name
		while x.payload:
			x = x.payload
			yield x.name

	@staticmethod
	def _layer_2_edge(packet):
		return packet[0].src, packet[0].dst, packet

	@staticmethod
	def _layer_3_edge(packet):
		if packet.haslayer(IP):
			return packet[1].src, packet[1].dst, packet

	@staticmethod
	def _layer_4_edge(packet):
		if any(map(lambda p: packet.haslayer(p), [TCP, UDP])):
			src = packet[1].src
			dst = packet[1].dst
			_ = packet[2]
			return "%s:%i" % (src, _.sport), "%s:%i" % (dst, _.dport), packet

	def draw(self, filename=None):
		self.graph.label ="Layer %d traffic graph for packets from %s" % (self.layer,str(self.args.pcaps))

		graph = self.get_graphviz_format()
		
		for node in graph.nodes():
			if node not in self.data:
				# node might be deleted, because it's not legit etc.
				continue
			snode = str(node)
			node.attr['shape'] = self.args.shape
			node.attr['fontsize'] = '10'
			node.attr['width'] = '0.5'
			node.attr['color'] = 'linen'
			node.attr['style'] = 'filled,rounded'
			if 'country' in self.data[snode]:
				country_label = self.data[snode]['country']
				city_label = self.data[snode]['city']
				nnode = self.lookup(snode)
				if nnode != snode:
					nodelab = '%s\n%s' % (nnode,snode)
				else:
					nodelab = snode
					
				if country_label != 'private':
					if city_label == 'private':
						nodelab += "\n(%s)" % (country_label)
					else:
						nodelab += "\n(%s, %s)" % (city_label, country_label)
				node.attr['label'] = nodelab
				if not (country_label == 'private'):
					node.attr['color'] = 'lightyellow'
					#TODO add color based on country or scan?
		for edge in graph.edges():
			connection = self.graph[edge[0]][edge[1]]
			edge.attr['label'] = 'transmitted: %i bytes\n%s ' % (connection['transmitted'], ' | '.join(connection['layers']))
			edge.attr['fontsize'] = '8'
			edge.attr['minlen'] = '2'
			edge.attr['penwidth'] = min(connection['connections'] * 1.0 / len(self.graph.nodes()), 2.0)
		graph.layout(prog=self.args.layoutengine)
		graph.draw(filename)

	def get_graphviz_format(self, filename=None):
		agraph = networkx.drawing.nx_agraph.to_agraph(self.graph)
		# remove packet information (blows up file size)
		for edge in agraph.edges():
			del edge.attr['packets']
		if filename:
			agraph.write(filename)
		return agraph
