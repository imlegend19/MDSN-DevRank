import pickle
import networkx as nx
import math

layer = 2

PATH_EDGES = "/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/definition_2/"

with open(PATH_EDGES + "layer" + str(layer) + "_edges_fc.txt", 'rb') as fp:
    edges = pickle.load(fp)

PATH_NEIGHBOUR = "/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/neighbours/definition_2/"

with open(PATH_NEIGHBOUR + "layer_" + str(layer) + "_neighbours.txt", 'rb') as fp:
    neighbors = pickle.load(fp)

graph = nx.DiGraph()
graph.add_edges_from(edges)

count = len(list(graph.nodes))
loc = {}
for i in graph.nodes:
    print("Remaining:", count)
    sub_graph = graph.subgraph(neighbors[i])

    total_degree = 0
    degrees = {}
    for (node, val) in sub_graph.degree:
        degrees[node] = val + 1
        total_degree += val + 1

    local_influence = 0
    for j in sub_graph.nodes:
        local_influence += (degrees[j] / total_degree) * math.log(degrees[j] / total_degree, 10)

    pi = len(neighbors[i]) / (total_degree + len(neighbors[i]))
    log_pi = math.log(pi, 10)
    local_influence += pi * log_pi

    loc[i] = -local_influence

    count -= 1

print(loc)

# with open("definition_1/layer_" + str(layer) + "_local_influence.txt", 'wb') as fp:
#     pickle.dump(loc, fp)

with open("definition_2/layer_" + str(layer) + "_local_influence.txt", 'wb') as fp:
    pickle.dump(loc, fp)
