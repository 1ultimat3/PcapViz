import networkx as nx
from util.decorators import edge_operator


@edge_operator
def create_digraph(edges):
    g = nx.DiGraph()
    g.add_edges_from(edges)
    return g


@edge_operator
def create_graph(edges):
    g = nx.Graph()
    g.add_edges_from(edges)
    return g


def symmetric_difference(graphs):
    new_g = graphs[0].__class__()
    edges = reduce(lambda s1, s2: s1.symmetric_difference(s2), _get_edge_list(graphs))
    new_g.add_edges_from(edges)
    return [new_g]


def difference(graphs):
    new_g = graphs[0].__class__()
    edges = reduce(lambda s1, s2: s1.difference(s2), _get_edge_list(graphs))
    new_g.add_edges_from(edges)
    return [new_g]


def _get_edge_list(graphs):
    return [set(g.edges()) for g in graphs]
