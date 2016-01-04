import unittest

from pcapviz.core import GraphManager
from pcapviz.sources import ScapySource

import os


class PcapProcessingTests(unittest.TestCase):

    def test_load_pcap(self):
        loaded = ScapySource.load(['test.pcap', 'test.pcap'])
        self.assertEqual(282, len(loaded))

    def test_build_graph_layer2(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=2)
        self.assertEqual(3, g.graph.number_of_edges())

    def test_build_graph_layer3(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets)
        self.assertEqual(8, g.graph.number_of_edges())

    def test_build_graph_layer4(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=4)
        self.assertEqual(36, g.graph.number_of_edges())

    def test_get_frequent_ips_in(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=3)
        ips = g.get_in_degree(print_stdout=True)
        self.assertIsNotNone(ips)

    def test_get_frequent_ips_out(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=3)
        ips = g.get_out_degree(print_stdout=True)
        self.assertIsNotNone(ips)

    def _draw(self, png, layer):
        try:
            os.remove(png)
        except OSError:
            pass
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=layer)
        g.draw(filename=png)
        self.assertTrue(os.path.exists(png))

    def test_layer2(self):
        self._draw('test2.png', 2)

    def test_layer3(self):
        self._draw('test3.png', 3)

    def test_layer4(self):
        self._draw('test4.png', 4)

    def test_retrieve_geoip(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=2)
        node = g.graph.nodes()[0]
        g._retrieve_node_info(node)
        self.assertNotIn('country', g.data[node])

    def test_retrieve_geoip(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=3)
        node = g.graph.nodes()[0]
        g._retrieve_node_info(node)
        self.assertIn('country', g.data[node])

    def test_retrieve_geoip(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=4)
        node = g.graph.nodes()[0]
        g._retrieve_node_info(node)
        self.assertIn('country', g.data[node])

    def test_graphviz(self):
        packets = ScapySource.load(['test.pcap'])
        g = GraphManager(packets, layer=3)
        self.assertIsNotNone(g.get_graphviz_format())


if __name__ == '__main__':
    unittest.main()