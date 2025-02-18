import pickle
from datetime import datetime
from itertools import permutations

import networkx as nx
import openpyxl
from local_settings_gnome import db

"""
Layer 3 Network: 

Edge between developers who commented on 2 bugs reported by same reporter.

Dataset Used : gnomebug
Table : bug
"""


def save_edges(edges):
    with open('layer3_edges_fc.txt', 'wb') as file:
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
    wb.save("layer3_ranks_fc.xlsx")

    print("Process Complete!")


def layer3(product_id):
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
            print("Fetching and setting up dict...")

            cur.execute("select distinctrow bug_id, reporter from test_bug_fixed_closed")
        else:
            cur.execute("select distinctrow bug_id, reporter from test_bug_fixed_closed where product_id="
                        + str(product_id))

        comp_bug = {}

        for i in cur.fetchall():
            if i[1].strip() not in comp_bug.keys():
                comp_bug[i[1].strip()] = [i[0]]
            else:
                val = comp_bug[i[1].strip()]
                val.append(i[0])
                comp_bug[i[1].strip()] = val

        if product_id is None:
            print("Length comp_bug", len(comp_bug))
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
            print("Setting up component-bug-who dict...")

        comp_bug_who = {}
        for i in comp_bug:
            val = comp_bug[i]
            who_s = set()
            for j in val:
                try:
                    who_lst = bug_who[j]
                    for k in who_lst:
                        who_s.add(k)
                except KeyError:
                    pass
            comp_bug_who[i] = who_s

        cbw_length = {}
        length = []

        if product_id is None:
            print("Calculating lengths...")

        edges = set()

        print("Setting up edges_normal...")
        edges = set()
        for i in comp_bug_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        if product_id is None:
            print("Writing layer 3 edges_normal to text file...")
            save_edges(edges)

            print("Process Successful! Total Edges =", len(edges))

        for i in edges:
            if i[0] in dev and i[1] in dev:
                pass
            else:
                print("NOOOOOOOO")

        graph = nx.DiGraph()

        try:
            graph.add_edges_from(list(edges))

            if product_id is None:
                print("Total edges_normal =", len(edges))
                print("Calculating eigenvector centrality...")

            centrality = nx.eigenvector_centrality(graph)

            ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
            ec.reverse()

            who_centrality = {}

            for i in who_centrality.values():
                print(i)

            with open("l3_centrality.txt", 'wb') as fp:
                pickle.dump(who_centrality, fp)

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

            print("Filled", len(graph.edges.data()), "edges_normal out of", len(edges))


layer3(None)
