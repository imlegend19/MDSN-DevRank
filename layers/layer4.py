import pickle
from datetime import datetime

import networkx as nx
import openpyxl
from local_settings import db

""" 
Layer 4 Network: 

Edge between developers who commented on 2 different bugs which belong to same operating system.

Dataset Used : gnomebug
Table : bug
"""


def save_edges(edges):
    with open('layer4_edges_fc.txt', 'wb') as file:
        pickle.dump(edges, file)


def save_ranks(developer, ec):
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
    wb.save("layer4_ranks_fc.xlsx")

    print("Process Complete!")


def layer4(product_id):
    with db:
        if product_id is None:
            print("Connected to db!")
            print("Fetching developers...")

        cur = db.cursor()
        cur.execute("SELECT DISTINCT who_id FROM who_ids_commenting_on_more_than_10_bugs")
        dev = []

        for i in cur.fetchall():
            dev.append(i[0])

        if product_id is None:
            cur.execute("select distinctrow bug_id, op_sys from test_bug_fixed_closed")
        else:
            cur.execute("select distinctrow bug_id, op_sys from test_bug_fixed_closed where product_id="
                        + str(product_id))

        os_bug = {}

        if product_id is None:
            print("Fetching and setting up dict...")

        for i in cur.fetchall():
            if i[1].strip() not in os_bug.keys():
                os_bug[i[1].strip()] = [i[0]]
            else:
                val = os_bug[i[1].strip()]
                val.append(i[0])
                os_bug[i[1].strip()] = val

        if product_id is None:
            print("Setup succeeded!")
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

        if product_id is None:
            print("Fetched!")
            print("Setting up os-bug-who dict...")

        os_bug_who = {}

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

        bug_who.clear()
        os_bug.clear()

        obw_length = {}
        length = []

        if product_id is None:
            print("Calculating lengths...")

        for i in os_bug_who:
            length.append(len(os_bug_who[i]))
            obw_length[len(os_bug_who[i])] = i

        length.sort(reverse=True)
        # del cbw_length[length.pop(0)]

        edges = set()

        if product_id is None:
            print("Setting up edges...")

        start = datetime.now().now()

        counter = 1
        for _ in length:
            i = obw_length[_]
            val = os_bug_who[i]

            if product_id is None:
                print("Ongoing =", counter, "- OS =", i, "- Total Length =", _, "- Total Edges =",
                      len(edges))

            for j in val:
                for k in val:
                    if j[0] != k[0]:
                        edges.add((j[1], k[1]))

            counter += 1

        end = datetime.now().time()

        if product_id is None:
            print("Start Time:", start, "End Time:", end)
            print("Writing layer 4 edges to text file...")

        if product_id is None:
            save_edges(edges)
            print("Process Successful! Total Edges =", len(edges))

        for i in edges:
            if i[0] in dev and i[1] in dev:
                pass
            else:
                print("NOOOOOOOO")

        if product_id is None:
            print("Building graph...")

        graph = nx.DiGraph()

        try:

            graph.add_edges_from(list(edges))

            if product_id is None:
                print("Total edges =", len(edges))
                print("Calculating eigenvector centrality...")

            centrality = nx.eigenvector_centrality(graph)

            ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
            ec.reverse()

            if product_id is None:
                print("Fetching developers...")
                cur.execute("SELECT DISTINCT who_id, who FROM test_comment_fixed_closed")

                developer = {}
                for i in cur.fetchall():
                    developer[i[0]] = i[1]

                save_ranks(developer, ec)
            else:
                sum_ec = 0

                for i in ec:
                    sum_ec += float(i[0])

                avg_centrality = sum_ec / len(ec)
                # print(product_id, ' : ', avg_centrality)

                return avg_centrality

        except Exception as e:

            print(e.args)
            print("Process Unsuccessful!")
