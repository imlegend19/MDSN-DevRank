import pickle

import networkx as nx

PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/edges/definition_1/"


def open_file(path):
    with open(path, 'rb') as fp:
        return pickle.load(fp)


def build_graph(edges):
    graph = nx.DiGraph()
    graph.add_edges_from(list(edges))

    nodes = list(graph.nodes)

    subgraphs = {}
    for i in nodes:
        sub_g = graph.subgraph(list(graph.neighbors(i)))
        subgraphs[i] = list(sub_g.edges)

    return subgraphs


def save_file(path, file):
    with open(path, 'wb') as fp:
        pickle.dump(file, fp)


layers = [open_file(PATH + "layer1_edges_fc.txt"), open_file(PATH + "layer2_edges_fc.txt"),
          open_file(PATH + "layer3_edges_fc.txt"), open_file(PATH + "layer4_edges_fc.txt")]

path = ["layer1_subgraph.txt", "layer2_subgraph.txt", "layer3_subgraph.txt", "layer4_subgraph.txt"]

for i in range(4):
    print("Ongoing", i)
    save_file("definition_1/" + path[i], build_graph(layers[i]))

print("Process Complete")
