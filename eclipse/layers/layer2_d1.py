import pickle
from itertools import permutations

import networkx as nx
import openpyxl
from local_settings_eclipse import db

"""
Layer 2 Network: 

Edge between developers who commented on 2 bugs which belong to same product.

Dataset Used : eclipse
Table : test_bugs_fixed_closed, test_longdescs_fixed_closed
"""

with db:
    print("Connected to db!")
    cur = db.cursor()

    print("Fetching developers...")
    cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

    dev = []
    for i in cur.fetchall():
        dev.append(i[0])

    cur.execute("select distinct who from test_longdescs_fixed_closed")

    filtered_who = []
    for i in cur.fetchall():
        filtered_who.append(i[0])

    cur.execute("SELECT distinctrow product_id, bug_id from test_bugs_fixed_closed")

    product_bug = {}
    for i in cur.fetchall():
        if i[0] in product_bug.keys():
            val = product_bug[i[0]]
            val.add(i[1])
            product_bug[i[0]] = val
        else:
            product_bug[i[0]] = {i[1]}

    cur.execute("SELECT distinctrow bug_id, who from test_longdescs_fixed_closed")
    bug_who = {}
    for i in cur.fetchall():
        if i[1] in filtered_who:
            if i[0] in bug_who.keys():
                if i[1] in dev:
                    val = bug_who[i[0]]
                    val.add(i[1])
                    bug_who[i[0]] = val
            else:
                if i[1] in dev:
                    bug_who[i[0]] = {i[1]}

    product_who = {}
    for i in product_bug:
        val = product_bug[i]
        who_s = set()
        for j in val:
            try:
                for k in bug_who[j]:
                    who_s.add(k)
            except KeyError:
                pass

        product_who[i] = who_s

    print("Setting up edges_normal...")
    edges = set()
    for i in product_who.values():
        if len(list(i)) > 1:
            edg = list(permutations(list(i), 2))
            for j in edg:
                if j[0] == j[1]:
                    print('err')
                edges.add(j)

    with open('layer2_edges_fc.txt', 'wb') as file:
        pickle.dump(edges, file)

    print("Saved edges_normal! Total edges_normal:", len(edges))

    graph = nx.DiGraph()
    graph.add_edges_from(list(edges))

    neighbours = {}
    for i in list(graph.nodes):
        lst = list(graph.neighbors(i))
        neighbours[i] = lst

    print(neighbours)

    path = "/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/neighbours/definition_1/"
    with open(path + "layer_2_neighbours.txt", 'wb') as fp:
        pickle.dump(neighbours, fp)

    # degrees = {}
    # for (node, val) in graph.degree:
    #     degrees[node] = val
    #
    # print(degrees)
    #
    # path = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/degree_centrality/definition_1/"
    # with open(path + "layer_2_degree.txt", 'wb') as fp:
    #     pickle.dump(degrees, fp)

    print("Calculating eigenvector centrality...")
    centrality = nx.eigenvector_centrality(graph)

    ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
    ec.reverse()

    who_centrality = {}

    for i in ec:
        who_centrality[i[1]] = i[0]

    with open("l2_d1_centrality.txt", 'wb') as fp:
        pickle.dump(who_centrality, fp)

    print("Setting up excel sheet...")
    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append(["Rank", "Id", "Centrality"])
    sheet.append(["", "", ""])

    print("Ranking developers...")

    rank = 1
    for i in ec:
        sheet.append([str(rank), i[1], i[0]])
        rank += 1

    print("Saving...")
    wb.save("layer2_ranks_fc.xlsx")

    print("Process Competed!")
