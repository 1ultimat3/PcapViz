from util.decorators import graph_operator
import matplotlib.pyplot as plt
import networkx as nx

counter = 0

@graph_operator
def draw_edges(graph, filename=None, figsize=(50, 50)):
    global counter
    plt.figure(figsize=figsize)
    nx.draw(graph, node_size=4500, width=3.0, with_labels=True, font_size=8, alpha=.5)
    if filename:
        plt.savefig("%s_%s" % (counter, filename))
        counter += 1
    return graph