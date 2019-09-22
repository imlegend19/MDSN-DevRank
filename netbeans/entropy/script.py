import networkx as nx
import pickle

layer = 2

PATH_LI = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/entropy/local_influence/definition_2/"
PATH_EDGES = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/definition_2/"
PATH_NEIGH = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/neighbours/definition_2/"

with open(PATH_LI + "layer_" + str(layer) + "_local_influence.txt", 'rb') as fp:
    li = pickle.load(fp)

with open(PATH_EDGES + "layer" + str(layer) + "_edges_fc.txt", 'rb') as fp:
    edges = pickle.load(fp)

with open(PATH_NEIGH + "layer_" + str(layer) + "_neighbours.txt", 'rb') as fp:
    neighbours = pickle.load(fp)

graph = nx.DiGraph()
graph.add_edges_from(edges)

cnt = len(graph.nodes)

indirect_influence = {}
for i in graph.nodes:
    print("Remaining:", cnt)
    nb = neighbours[i]
    hop_2_neighbours = set()

    for j in nb:
        for k in neighbours[j]:
            if k not in nb:
                hop_2_neighbours.add(k)

    neighs = {}
    for j in hop_2_neighbours:
        paths = nx.all_shortest_paths(graph, i, j)

        counter = 0
        pairs = set()
        for k in list(paths):
            if len(k) == 3:
                pairs.add((i, k[1]))
                counter += 1

        neighs[j] = [pairs, counter]

    ii = 0
    for j in neighs:
        influence = 0
        for k in neighs[j][0]:
            influence += li[k[0]] * li[k[1]]

        try:
            influence /= neighs[j][1]
        except ZeroDivisionError:
            print(j)

        ii += influence

    ii /= len(neighs.keys())
    indirect_influence[i] = ii

    cnt -= 1

with open("definition_2/indirect_influence_layer_" + str(layer) + ".txt", 'wb') as fp:
    pickle.dump(indirect_influence, fp)
