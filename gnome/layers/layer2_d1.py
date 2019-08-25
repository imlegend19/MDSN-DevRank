import pickle
from itertools import permutations
import networkx as nx
import openpyxl
from local_settings_gnome import db

"""
Layer 2 Network: 

Edge between developers who commented on 2 bugs which belong to same product.

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

    product_bug = {}

    print("Setting up product-bug...")
    cur.execute("SELECT distinctrow product_id, bug_id FROM test_bug_fixed_closed")

    for i in cur.fetchall():
        if i[0] in product_bug.keys():
            val = product_bug[i[0]]
            val.append(i[1])
            product_bug[i[0]] = val
        else:
            product_bug[i[0]] = [i[1]]

    print("Fetched!")

    # print("Writing product_bug to text file...")
    #
    # with open('layer2_product_bug.txt', 'wb') as file:
    #     pickle.dump(product_bug, file)

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

    print("Fetched!")
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

    with open("l2_d1_centrality.txt", 'wb') as fp:
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
