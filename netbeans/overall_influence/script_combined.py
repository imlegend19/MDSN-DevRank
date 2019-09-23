import pickle
import networkx as nx

w1 = 0.6
w2 = 0.4

PATH_LI = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/entropy/local_influence/"
PATH_II = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/entropy/"
PATH_EDGES = "/home/niit1/PycharmProjects/Data-Mining-Research/netbeans/edges/"

with open(PATH_LI + "combined_local_influence_d1.txt", 'rb') as fp:
    li = pickle.load(fp)

with open(PATH_II + "indirect_influence_layer_d1.txt", 'rb') as fp:
    ii = pickle.load(fp)

with open(PATH_EDGES + "edges_d1.txt", 'rb') as fp:
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
    except ZeroDivisionError:
        print(i)

with open("overall_influence_combined_d1.txt", 'wb') as fp:
    pickle.dump(overall_influence, fp)

print("Average:", round(sum(oi) / len(oi), 1))
