import pickle
from datetime import datetime

import networkx as nx
import openpyxl

from local_settings_eclipse import db

"""
Layer 2 Network: 

Edge between developers who commented on 2 different bugs which belong to 
same product and component.

Dataset Used : eclipse
Table : test_bugs_fixed_closed, test_longdescs_fixed_closed
"""

with db:
    print("Connected to db!")
    cur = db.cursor()

    cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

    dev = []
    for i in cur.fetchall():
        dev.append(i[0])

    product_component_bug = {}

    print("Setting up product-bug...")
    cur.execute("SELECT distinctrow product_id, component_id, bug_id FROM test_bugs_fixed_closed")

    for i in cur.fetchall():
        if (i[0], i[1]) in product_component_bug.keys():
            val = product_component_bug[(i[0], i[1])]
            val.append(i[2])
            product_component_bug[(i[0], i[1])] = val
        else:
            product_component_bug[(i[0], i[1])] = [i[2]]

    print("Fetched!")

    cur.execute("select who from test_longdescs_fixed_closed")

    filtered_who = []
    for i in cur.fetchall():
        filtered_who.append(i[0])

    print("Setting up dict for who_id's who have commented on same bug...")

    cur.execute("SELECT distinctrow bug_id, who FROM test_longdescs_fixed_closed")
    bug_who = {}

    bugs_taken = []
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
            bugs_taken.append(i[0])

    with open("bugs_taken3.txt", 'wb') as fp:
        pickle.dump(bugs_taken, fp)

    print("Fetched!")

    prod_bug_who = {}

    print("Setting up product-bug-who dict...")
    for i in product_component_bug:
        val = product_component_bug[i]
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
    product_component_bug.clear()

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

        print("Ongoing =", counter, "- Product - Component =", i, "- Total Length =", _, "- Total Edges =",
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
    centrality = nx.eigenvector_centrality(graph)

    ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
    ec.reverse()

    who_centrality = {}

    for i in ec:
        who_centrality[i[1]] = i[0]

    with open("l2_d2_centrality.txt", 'wb') as fp:
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
