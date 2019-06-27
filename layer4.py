from datetime import datetime

import networkx as nx
import openpyxl
import pymysql

db = pymysql.connect(host='localhost',
                     user='mahen',
                     password='#imlegend19',
                     db='master')

"""
Layer 4 Network: 

Edge between developers who commented on 2 different bugs which belong to same operating system.

Dataset Used : gnomebug
Table : bug
"""
with db:
    print("Connected to db!")
    cur = db.cursor()

    cur.execute("select distinct bug_id, op_sys from test_bug")

    os_bug = {}

    print("Fetching and setting up dict...")
    for i in cur.fetchall():
        if i[1].strip() not in os_bug.keys():
            os_bug[i[1].strip()] = [i[0]]
        else:
            val = os_bug[i[1].strip()]
            val.append(i[0])
            os_bug[i[1].strip()] = val

    print("Setup succeeded!")

    # with open('layer4_os_bug.txt', 'wb') as file:
    #     pickle.dump(os_bug, file)

    print("Setting up dict for who_id's who have commented on same bug...")

    cur.execute("SELECT bug_id, who_id FROM comment")
    bug_who = {}

    for i in cur.fetchall():
        if i[0] in bug_who.keys():
            val = bug_who[i[0]]
            val.add(i[1])
            bug_who[i[0]] = val
        else:
            bug_who[i[0]] = {i[1]}

    print("Fetched!")

    os_bug_who = {}

    print("Setting up os-bug-who dict...")
    for i in os_bug:
        val = os_bug[i]
        dic_val = []
        for j in val:
            try:
                who_lst = bug_who[j]
                for k in who_lst:
                    dic_val.append((j, k))
            except KeyError:
                pass
        os_bug_who[i] = dic_val

    # print("Writing component_bug_who to text file...")
    #
    # with open('layer3_component_bug_who.txt', 'w') as file:
    #     file.write(json.dumps(comp_bug_who))

    print("Clearing variables...")

    bug_who.clear()
    os_bug.clear()

    obw_length = {}
    length = []

    print("Calculating lengths...")
    for i in os_bug_who:
        length.append(len(os_bug_who[i]))
        obw_length[len(os_bug_who[i])] = i

    length.sort(reverse=True)
    # del cbw_length[length.pop(0)]

    print(length)

    edges = set()

    print("Setting up edges...")

    start = datetime.now().now()

    counter = 1
    for _ in length:
        i = obw_length[_]
        val = os_bug_who[i]

        print("Ongoing =", counter, "- OS =", i, "- Total Length =", _, "- Total Edges =",
              len(edges))

        for j in val:
            for k in val:
                if j[0] != k[0]:
                    edges.add((j[1], k[1]))
        counter += 1

    end = datetime.now().time()

    print("Start Time:", start, "End Time:", end)

    # print("Writing layer 4 edges to text file...")
    #
    # with open('layer4_edges.txt', 'wb') as file:
    #     pickle.dump(edges, file)

    print("Process Successful! Total Edges =", len(edges))

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
        wb.save("layer4_ranks.xlsx")

        print("Process Complete!")

    except Exception as e:

        print(e.args)
        print("Process Unsuccessful!")
