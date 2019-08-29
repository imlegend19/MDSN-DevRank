import pickle
from itertools import permutations

import networkx as nx
import openpyxl
from local_settings_eclipse import db

"""
Layer 3 Network: 

Edge between developers who commented on 2 bugs reported by same reporter.

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

    cur.execute("SELECT distinctrow reporter, bug_id from test_bugs_fixed_closed")

    reporter_bug = {}
    for i in cur.fetchall():
        if i[0] in reporter_bug.keys():
            val = reporter_bug[i[0]]
            val.add(i[1])
            reporter_bug[i[0]] = val
        else:
            reporter_bug[i[0]] = {i[1]}

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

    reporter_who = {}
    for i in reporter_bug:
        val = reporter_bug[i]
        who_s = set()
        for j in val:
            try:
                for k in bug_who[j]:
                    who_s.add(k)
            except KeyError:
                pass

        reporter_who[i] = who_s

    print("Setting up edges_normal...")
    edges = set()
    for i in reporter_who.values():
        if len(list(i)) > 1:
            edg = list(permutations(list(i), 2))
            for j in edg:
                if j[0] == j[1]:
                    print('err')
                edges.add(j)

    with open('layer3_edges_fc.txt', 'wb') as file:
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

    with open("l3_centrality.txt", 'wb') as fp:
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
    wb.save("layer3_ranks_fc.xlsx")

    print("Process Competed!")
