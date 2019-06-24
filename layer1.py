from itertools import permutations

import pymysql
import openpyxl
import networkx as nx

db = pymysql.connect(host='localhost',
                     user='mahen',
                     password='#imlegend19',
                     db='master')

"""
Layer 1 Network: 

Edge between developers who commented on same bug.

Dataset Used : gnomebug
Table : comment
"""
with db:
    print("Connected to db!")
    cur = db.cursor()

    # print("Fetching all rows...")
    # cur.execute("SELECT * FROM comment")
    #
    # rows = cur.fetchall()

    bug_who = {}

    print("Setting up dict for who_id's who have commented on same bug...")

    cur.execute("SELECT bug_id, who_id FROM comment")

    # FMT = '%H:%M:%S'
    # start = datetime.now().time()

    for i in cur.fetchall():
        if i[0] in bug_who.keys():
            val = bug_who[i[0]]
            val.add(i[1])
            bug_who[i[0]] = val
        else:
            bug_who[i[0]] = {i[1]}

    print("Fetched!")

    print("Setting up edges...")
    edges = set()
    for i in bug_who.values():
        if len(list(i)) > 1:
            edg = list(permutations(list(i), 2))
            for j in edg:
                edges.add(j)

    # with open('layer1_edges.txt', 'w') as file:
    #     file.write(str(edges))

    graph = nx.DiGraph()
    graph.add_edges_from(list(edges))

    print("Calculating eigenvector centrality...")
    centrality = nx.eigenvector_centrality(graph)

    ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
    ec.reverse()

    # print("Saving centrality...")
    # with open('layer1_centrality.txt', 'w') as file:
    #     file.write(str(ec))

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
    wb.save("layer1_ranks.xlsx")

    print("Process Competed!")
