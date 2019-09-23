import pickle
import networkx as nx

with open("/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/edges_d2.txt", 'rb') as fp:
    edges = pickle.load(fp)

graph = nx.DiGraph()
graph.add_edges_from(list(edges))

neighbours = {}
for i in list(graph.nodes):
    lst = list(graph.neighbors(i))
    neighbours[i] = lst

print(neighbours)
path = "/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/neighbours/"
with open(path + "all_layer_neighbours_d2.txt", 'wb') as fp:
    pickle.dump(neighbours, fp)

print("Process Competed!")
