import pickle
from datetime import datetime
from itertools import permutations

import networkx as nx
import openpyxl
from local_settings_gnome import db

"""
Layer 2 Network: 

Edge between developers who commented on 2 bugs which belong to 
same product and component.

Dataset Used : gnomebug
Table : bug
"""

with db:
    print("Connected to db!")
    cur = db.cursor()

    print("Fetching developers...")
    cur.execute("SELECT DISTINCT who_id FROM who_ids_commenting_on_more_than_10_bugs")
    dev = []

    for i in cur.fetchall():
        dev.append(i[0])

    print("Setting up dict for who_id's who have commented on same bug...")

    cur.execute("SELECT distinctrow bug_id, who_id FROM test_comment_fixed_closed")
    bug_who = {}
    for i in cur.fetchall():
        if i[0] in bug_who.keys():
            if i[1] in dev:
                val = bug_who[i[0]]
                val.add(i[1])
                bug_who[i[0]] = val
        else:
            if i[1] in dev:
                bug_who[i[0]] = {i[1]}

    product_component_bug = {}

    print("Setting up product-bug...")
    cur.execute("SELECT distinctrow product_id, component, bug_id FROM test_bug_fixed_closed")

    for i in cur.fetchall():
        if i[2] in bug_who:
            if (i[0], i[1].strip()) in product_component_bug.keys():
                val = product_component_bug[(i[0], i[1].strip())]
                val.append(i[2])
                product_component_bug[(i[0], i[1].strip())] = val
            else:
                product_component_bug[(i[0], i[1].strip())] = [i[2]]

    print("Fetched!")

    prod_comp_who = {}
    print("Setting up product-bug-who dict...")
    for i in product_component_bug:
        val = product_component_bug[i]
        who_s = set()
        for j in val:
            try:
                who_lst = bug_who[j]
                for k in who_lst:
                    who_s.add(k)
            except KeyError:
                pass
        prod_comp_who[i] = who_s

    edges = set()
    for i in prod_comp_who.values():
        if len(list(i)) > 1:
            edg = list(permutations(list(i), 2))
            for j in edg:
                if j[0] == j[1]:
                    print('err')
                edges.add(j)

    print("Writing layer 2 edges_normal to text file...")
    with open('layer2_edges_fc.txt', 'wb') as file:
        pickle.dump(edges, file)

    print("Process Successful! Total Edges =", len(edges))

    for i in edges:
        if i[0] in dev and i[1] in dev:
            pass
        else:
            print("NOOOOOOOO")

    print("Building graph...")
    graph = nx.DiGraph()
    graph.add_edges_from(list(edges))

    print("Total edges_normal =", len(edges))

    print("Calculating eigenvector centrality...")
    centrality = nx.eigenvector_centrality(graph)

    ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
    ec.reverse()

    who_centrality = {}

    for i in ec:
        who_centrality[i[1]] = i[0]

    with open("l2_d2_centrality.txt", 'wb') as fp:
        pickle.dump(who_centrality, fp)

    print("Fetching developers...")
    cur.execute("SELECT DISTINCT who_id, who FROM comment")

    developer = {}
    for i in cur.fetchall():
        developer[i[0]] = i[1]

    print("Setting up excel sheet...")
    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append(["Rank", "Id", "Who", "Centrality"])
    sheet.append(["", "", "", ""])

    print("Ranking developers...")

    rank = 1
    for i in ec:
        sheet.append([str(rank), i[1], developer[i[1]], i[0]])
        rank += 1

    print("Saving...")
    wb.save("layer2_ranks_fc.xlsx")

    print("Process Complete!")
