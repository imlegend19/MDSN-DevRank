import pickle
from datetime import datetime

import networkx as nx
import openpyxl
from local_settings_eclipse import db

"""
Layer 2 Network: 

Edge between developers who commented on 2 different bugs which belong to same product.

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

    product_bug = {}

    print("Setting up product-bug...")
    cur.execute("SELECT distinctrow product_id, bug_id FROM test_bugs_fixed_closed")

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

    cur.execute("SELECT distinctrow bug_id, who FROM test_longdescs_fixed_closed")
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

    prod_bug_who = {}

    print("Setting up product-bug-who dict...")
    for i in product_bug:
        val = product_bug[i]
        dic_val = []
        for j in val:
            try:
                who_lst = bug_who[j]
                for k in who_lst:
                    dic_val.append((j, k))
            except KeyError:
                pass
        prod_bug_who[i] = dic_val

    print("Clearing variables...")

    bug_who.clear()
    product_bug.clear()

    pbw_length = {}
    length = []

    print("Calculating lengths...")
    for i in prod_bug_who:
        length.append(len(prod_bug_who[i]))
        pbw_length[len(prod_bug_who[i])] = i

    length.sort(reverse=True)
    # del pbw_length[length.pop(0)]

    print(length)

    edges = set()

    print("Setting up edges_normal...")

    start = datetime.now().now()

    counter = 1
    for _ in length:
        i = pbw_length[_]
        val = prod_bug_who[i]

        print("Ongoing =", counter, "- Product =", i, "- Total Length =", _, "- Total Edges =",
              len(edges))

        for j in val:
            for k in val:
                if j[1] != k[1]:
                    edges.add((j[1], k[1]))

        counter += 1

    end = datetime.now().time()

    print("Start Time:", start, "End Time:", end)

    print("Writing layer 2 edges_normal to text file...")

    with open('layer2_edges_fc.txt', 'wb') as file:
        pickle.dump(edges, file)

    print("Process Successful! Total Edges =", len(edges))

    print("Building graph...")
    graph = nx.DiGraph()
    graph.add_edges_from(list(edges))

    print("Total edges_normal =", len(edges))

    print("Calculating eigenvector centrality...")
    centrality = nx.eigenvector_centrality_numpy(graph)

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

    print("Process Complete!")
