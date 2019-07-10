import pickle
from datetime import datetime
import networkx as nx
import openpyxl

from local_settings import db

"""
Layer 5 Network:

Edge between developers who commented on 2 different bugs which have the same bug severity.

Dataset Used : gnomebug
Table : test_bug
"""

with db:
    print("Connected to db!")
    cur = db.cursor()

    print("Fetching developers...")
    cur.execute("SELECT DISTINCT who_id FROM who_ids_commenting_on_more_than_10_bugs")
    dev = []

    for i in cur.fetchall():
        dev.append(i[0])

    cur.execute("select distinctrow bug_id, priority from test_bug_fixed_closed")

    priority_bug = {}

    print("Fetching and setting up dict...")
    for i in cur.fetchall():
        if i[1].strip() not in priority_bug.keys():
            priority_bug[i[1].strip()] = [i[0]]
        else:
            val = priority_bug[i[1].strip()]
            val.append(i[0])
            priority_bug[i[1].strip()] = val

    print("Setup succeeded!")

    # with open('layer5_severity_bug.txt', 'wb') as file:
    #     pickle.dump(severity_bug, file)

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

    priority_bug_who = {}

    print("Setting up severity-bug-who dict...")
    for i in priority_bug:
        val = priority_bug[i]
        dic_val = []
        for j in val:
            try:
                who_lst = bug_who[j]
                for k in who_lst:
                    dic_val.append((j, k))
            except KeyError:
                pass
        priority_bug_who[i] = dic_val

    print("Clearing variables...")

    bug_who.clear()
    priority_bug.clear()

    pbw_length = {}
    length = []

    print("Calculating lengths...")
    for i in priority_bug_who:
        length.append(len(priority_bug_who[i]))
        pbw_length[len(priority_bug_who[i])] = i

    length.sort(reverse=True)
    # del pbw_length[length.pop(0)]

    print(length)

    edges = set()

    print("Setting up edges...")

    start = datetime.now().now()

    counter = 1
    for _ in length:
        i = pbw_length[_]
        val = priority_bug_who[i]

        print("Ongoing =", counter, "- Priority =", i, "- Total Length =", _, "- Total Edges =",
              len(edges))

        for j in val:
            for k in val:
                if j[0] != k[0]:
                    edges.add((j[1], k[1]))

        counter += 1

    end = datetime.now().time()

    print("Start Time:", start, "End Time:", end)

    print("Writing layer 6 edges to text file...")

    with open('layer6_edges_fc.txt', 'wb') as file:
        pickle.dump(edges, file)

    print("Process Successful! Total Edges =", len(edges))

    for i in edges:
        if i[0] in dev and i[1] in dev:
            pass
        else:
            print("NO!")

    print("Building graph...")
    graph = nx.DiGraph()

    try:

        graph.add_edges_from(list(edges))

        print("Total edges =", len(edges))

        print("Calculating eigenvector centrality...")
        centrality = nx.eigenvector_centrality(graph)

        ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
        ec.reverse()

        print("Fetching developers...")
        cur.execute("SELECT DISTINCT who_id, who FROM test_comment_fixed_closed")

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
        wb.save("layer6_ranks_fc.xlsx")

        print("Process Complete!")

    except Exception as e:

        print(e.args)
        print("Process Unsuccessful!")
