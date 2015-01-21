import networkx as nx
from collections import OrderedDict
from util.decorators import graph_operator


@graph_operator
def get_frequent_ips(graph, print_stdout=True):
    unsorted_degrees = nx.degree(graph)
    sorted_degrees = OrderedDict(sorted(unsorted_degrees.items(), key=lambda t: t[1], reverse=True))
    for i in sorted_degrees:
        if print_stdout:
            print sorted_degrees[i], i
    return sorted_degrees

