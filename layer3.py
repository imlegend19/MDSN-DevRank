from datetime import datetime

import networkx as nx
import openpyxl
import pymysql

db = pymysql.connect(host='localhost',
                     user='mahen',
                     password='#imlegend19',
                     db='master')

"""
Layer 3 Network: 

Edge between developers who commented on 2 different bugs which belong to same component.

Dataset Used : gnomebug
Table : bug
"""
with db:
    print("Connected to db!")
    cur = db.cursor()

    print("Fetching and setting up dict...")
    cur.execute("select distinct bug_id, component from test_bug")
    comp_bug = {}

    for i in cur.fetchall():
        if i[1].strip() not in comp_bug.keys():
            comp_bug[i[1].strip()] = [i[0]]
        else:
            val = comp_bug[i[1].strip()]
            val.append(i[0])
            comp_bug[i[1].strip()] = val

    print("Setup succeeded!")

    # with open('layer3_component_bug.txt', 'w') as file:
    #     file.write(json.dumps(comp_bug))

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

    comp_bug_who = {}

    print("Setting up component-bug-who dict...")
    for i in comp_bug:
        val = comp_bug[i]
        dic_val = []
        for j in val:
            try:
                who_lst = bug_who[j]
                for k in who_lst:
                    dic_val.append((j, k))
            except KeyError:
                pass
        comp_bug_who[i] = dic_val

    # print("Writing component_bug_who to text file...")
    #
    # with open('layer3_component_bug_who.txt', 'w') as file:
    #     file.write(json.dumps(comp_bug_who))

    print("Clearing variables...")

    bug_who.clear()
    comp_bug.clear()

    cbw_length = {}
    length = []

    print("Calculating lengths...")
    for i in comp_bug_who:
        length.append(len(comp_bug_who[i]))
        cbw_length[len(comp_bug_who[i])] = i

    length.sort(reverse=True)
    # del cbw_length[length.pop(0)]

    print(length)

    edges = set()

    print("Setting up edges...")

    start = datetime.now().now()

    counter = 1
    for _ in length:
        i = cbw_length[_]
        val = comp_bug_who[i]

        print("Ongoing =", counter, "- Component =", i, "- Total Length =", _, "- Total Edges =",
              len(edges))

        for j in val:
            for k in val:
                if j[0] != k[0]:
                    edges.add((j[1], k[1]))
        counter += 1

    end = datetime.now().time()

    print("Start Time:", start, "End Time:", end)

    # print("Writing layer 3 edges to text file...")
    #
    # with open('layer3_edges.txt', 'wb') as file:
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
        wb.save("layer3_ranks.xlsx")

        print("Process Complete!")

    except Exception as e:

        print(e.args)
        print("Process Unsuccessful!")

        print("Filled", len(graph.edges.data()), "edges out of", len(edges))
