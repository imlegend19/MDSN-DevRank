import pickle
from datetime import datetime
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

    cur.execute("SELECT distinctrow product_id, who from test_longdescs_fixed_closed")

    # FMT = '%H:%M:%S'
    # start = datetime.now().time()

    product_who = {}
    bugs_taken = []
    for i in cur.fetchall():
        if i[1] in filtered_who:
            if i[0] in product_who.keys():
                if i[1] in dev:
                    val = product_who[i[0]]
                    val.add(i[1])
                    product_who[i[0]] = val
            else:
                if i[1] in dev:
                    product_who[i[0]] = {i[1]}
            bugs_taken.append(i[0])

    with open("bugs_taken.txt", 'wb') as fp:
        pickle.dump(bugs_taken, fp)

    print("Fetching bugs from test_bug...")
    cur.execute("SELECT distinct bug_id FROM test_bugs_fixed_closed")

    bugs = []
    for i in cur.fetchall():
        bugs.append(i[0])

    print("Fetched!")
    print("Updating bug_who...")

    for i in list(product_who.keys()):
        if i not in bugs:
            print("#############", i)
            del product_who[i]

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

    print("Calculating eigenvector centrality...")
    centrality = nx.eigenvector_centrality(graph)

    ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
    ec.reverse()

    who_centrality = {}

    for i in ec:
        who_centrality[i[1]] = i[0]

    with open("l2_centrality.txt", 'wb') as fp:
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
