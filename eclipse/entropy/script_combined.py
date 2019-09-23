import pickle
import networkx as nx

PATH_LI = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/entropy/local_influence/combined_local_influence_d1.txt"
PATH_EDGES = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/edges_d1.txt"
PATH_NEIGH = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/neighbours/all_layer_neighbours_d1.txt"

with open(PATH_LI, 'rb') as fp:
    li = pickle.load(fp)

with open(PATH_EDGES, 'rb') as fp:
    edges = pickle.load(fp)

with open(PATH_NEIGH, 'rb') as fp:
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

with open("indirect_influence_layer_d1.txt", 'wb') as fp:
    pickle.dump(indirect_influence, fp)
