import pickle

layer = 2

PATH_LI = "/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/entropy/local_influence/definition_2/"
PATH_EDGES = "/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/definition_2/"
PATH_NEIGH = "/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/neighbours/definition_2/"

with open(PATH_LI + "layer_" + str(layer) + "_local_influence.txt", 'rb') as fp:
    li = pickle.load(fp)

with open(PATH_EDGES + "layer" + str(layer) + "_edges_fc.txt", 'rb') as fp:
    edges = pickle.load(fp)

with open(PATH_NEIGH + "layer_" + str(layer) + "_neighbours.txt", 'rb') as fp:
    neighbours = pickle.load(fp)

graph = {}
for i in edges:
    if i[0] in graph:
        val = graph[i[0]]
        val.append(i[1])
        graph[i[0]] = val
    else:
        graph[i[0]] = [i[1]]

indirect_influence = {}
for i in graph.keys():
    sg = graph[i]

    hop2_neighs_dict = {}
    hop2_neighs = set()
    for j in sg:
        ssg = graph[j]

        for k in ssg:
            if k in sg or k == i:
                pass
            else:
                hop2_neighs.add(k)

        hop2_neighs_dict[j] = ssg

    ii = 0
    tot = 0
    for j in hop2_neighs:
        pairwise_li = 0
        cnt = 0
        for k in hop2_neighs_dict:
            if j in hop2_neighs_dict[k]:
                pairwise_li += li[i] * li[k]
                cnt += 1
        ii += pairwise_li / cnt
        tot += 1

    try:
        indirect_influence[i] = ii / tot
    except ZeroDivisionError:
        print(i)


with open("indirect_influence_" + str(layer) + ".txt", 'wb') as fp:
    pickle.dump(indirect_influence, fp)
