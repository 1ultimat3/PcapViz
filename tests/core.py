import unittest
import sys
import os

# finesse the imports - ugh - so we can run from the tests directory

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from pcapviz.core import GraphManager
from pcapviz.sources import ScapySource
from main import args
args.pcaps = 'test.pcap'

import os


class PcapProcessingTests(unittest.TestCase):

    def test_load_pcap(self):
        loaded = ScapySource.load(['test.pcap', 'test.pcap'])
        self.assertEqual(282, len(loaded))

    def test_build_graph_layer2(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=2,args=args)
        self.assertEqual(3, g.graph.number_of_edges())

    def test_build_graph_layer3(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets,args=args)
        self.assertEqual(8, g.graph.number_of_edges())

    def test_build_graph_layer4(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=4,args=args)
        self.assertEqual(36, g.graph.number_of_edges())

    def test_get_frequent_ips_in(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=3, args=args)
        ips = g.get_in_degree(print_stdout=True)
        self.assertIsNotNone(ips)

    def test_get_frequent_ips_out(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=3, args=args)
        ips = g.get_out_degree(print_stdout=True)
        self.assertIsNotNone(ips)

    def _draw(self, png, layer):
        try:
            os.remove(png)
        except OSError:
            pass
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=layer, args=args)
        g.draw(filename=png)
        self.assertTrue(os.path.exists(png))

    def test_layer2(self):
        self._draw('test2.png', 2)

    def test_layer3(self):
        self._draw('test3.png', 3)

    def test_layer4(self):
        self._draw('test4.png', 4)

    def test_retrieve_geoip2(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=2, args=args)
        node = list(g.data.keys())[0]
        g._retrieve_node_info(node)
        self.assertNotIn('country', g.data[node])

    def test_retrieve_geoip3(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=3, args=args)
        node = list(g.data.keys())[0]
        g._retrieve_node_info(node)
        self.assertIn('country', g.data[node])

    def test_retrieve_geoip4(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=4, args=args)
        node = list(g.data.keys())[0]
        g._retrieve_node_info(node)
        self.assertIn('country', g.data[node])

    def test_graphviz(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=3,args=args)
        self.assertIsNotNone(g.get_graphviz_format())


if __name__ == '__main__':
    unittest.main()
