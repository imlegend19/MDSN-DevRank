import pickle
import networkx as nx

layer = 2

w1 = 0.6
w2 = 0.4

PATH_LI = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/entropy/local_influence/definition_2/"
PATH_II = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/indirect_influence/definition_2/"
PATH_EDGES = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/definition_2/"

with open(PATH_LI + "layer_" + str(layer) + "_local_influence.txt", 'rb') as fp:
    li = pickle.load(fp)

with open(PATH_II + "indirect_influence_" + str(layer) + ".txt", 'rb') as fp:
    ii = pickle.load(fp)

with open(PATH_EDGES + "layer" + str(layer) + "_edges_fc.txt", 'rb') as fp:
    edges = pickle.load(fp)

graph = nx.DiGraph()
graph.add_edges_from(edges)

oi = []
overall_influence = {}
for i in graph.nodes:
    try:
        overall_influence[i] = w1*li[i] + w2*ii[i]
        oi.append(1 - (max(ii[i], li[i]) / min(ii[i], li[i])))
    except KeyError:
        print(i)

with open("overall_influence_layer_" + str(layer) + ".txt", 'wb') as fp:
    pickle.dump(overall_influence, fp)

print("Average:", round(sum(oi) / len(oi), 1))
