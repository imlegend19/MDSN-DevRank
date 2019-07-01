import pickle
from itertools import permutations

import openpyxl
import networkx as nx
from local_settings import db

"""
Layer 1 Network: 

Edge between developers who commented on same bug.

Dataset Used : gnomebug
Table : comment
"""

with db:
    print("Connected to db!")
    cur = db.cursor()

    print("Fetching developers...")
    cur.execute("SELECT DISTINCT who_id FROM who_ids_commenting_on_more_than_10_bugs")
    dev = []

    for i in cur.fetchall():
        dev.append(i[0])

    bug_who = {}

    print("Setting up dict for who_id's who have commented on same bug...")

    cur.execute("SELECT distinctrow bug_id, who_id FROM test_comment")

    # FMT = '%H:%M:%S'
    # start = datetime.now().time()

    for i in cur.fetchall():
        if i[0] in bug_who.keys():
            if i[1] in dev:
                val = bug_who[i[0]]
                val.add(i[1])
                bug_who[i[0]] = val
        else:
            if i[1] in dev:
                bug_who[i[0]] = {i[1]}

    print("Fetching bugs from test_bug...")
    cur.execute("SELECT distinct bug_id FROM test_bug")

    bugs = []
    for i in cur.fetchall():
        bugs.append(i[0])

    print("Fetched!")

    print("Updating bug_who...")
    for i in list(bug_who.keys()):
        if i not in bugs:
            del bug_who[i]

    print("Setting up edges...")
    edges = set()
    for i in bug_who.values():
        if len(list(i)) > 1:
            edg = list(permutations(list(i), 2))
            for j in edg:
                edges.add(j)

    with open('layer1_edges.txt', 'wb') as file:
        pickle.dump(edges, file)

    for i in edges:
        if i[0] in dev and i[1] in dev:
            print('YES')
        else:
            print("NOOOOOOOO")

    print("Saved edges! Total edges:", len(edges))

    graph = nx.DiGraph()
    graph.add_edges_from(list(edges))

    print("Calculating eigenvector centrality...")
    centrality = nx.eigenvector_centrality(graph)

    ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
    ec.reverse()

    print("Fetching developers...")
    cur.execute("SELECT DISTINCT who_id, who FROM test_comment")

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
    wb.save("layer1_ranks.xlsx")

    print("Process Competed!")
