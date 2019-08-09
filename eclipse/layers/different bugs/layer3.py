import pickle
from datetime import datetime

import networkx as nx
import openpyxl
from local_settings_eclipse import db

"""
Layer 3 Network: 

Edge between developers who commented on 2 different bugs reported by same reporter.

Dataset Used : eclipse
Table : test_bugs_fixed_closed, test_longdescs_fixed_closed
"""


def save_edges(edges):
    with open('layer3_edges_fc.txt', 'wb') as file:
        pickle.dump(edges, file)


def save_ranks(ec):
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

    print("Process Complete!")


def layer3(product_id):
    with db:
        if product_id is None:
            print("Connected to db!")
            print("Fetching developers...")

        cur = db.cursor()

        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        if product_id is None:
            print("Fetching and setting up dict...")

            cur.execute("select distinctrow bug_id, reporter from test_bugs_fixed_closed")
        else:
            cur.execute("select distinctrow bug_id, reporter from test_bugs_fixed_closed where product_id="
                        + str(product_id))

        comp_bug = {}

        for i in cur.fetchall():
            if i[1] not in comp_bug.keys():
                comp_bug[i[1]] = [i[0]]
            else:
                val = comp_bug[i[1]]
                val.append(i[0])
                comp_bug[i[1]] = val

        if product_id is None:
            print("Length comp_bug", len(comp_bug))
            print("Setup succeeded!")

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

        with open("bugs_taken4.txt", 'wb') as fp:
            pickle.dump(bugs_taken, fp)

        if product_id is None:
            print("Fetched!")
            print("Setting up component-bug-who dict...")

        comp_bug_who = {}

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

        bug_who.clear()
        comp_bug.clear()

        cbw_length = {}
        length = []

        if product_id is None:
            print("Calculating lengths...")

        for i in comp_bug_who:
            length.append(len(comp_bug_who[i]))
            cbw_length[len(comp_bug_who[i])] = i

        length.sort(reverse=True)
        # del cbw_length[length.pop(0)]

        edges = set()

        if product_id is None:
            print("Setting up edges_normal...")

        start = datetime.now().now()

        counter = 1
        for _ in length:
            i = cbw_length[_]
            val = comp_bug_who[i]

            if product_id is None:
                print("Ongoing =", counter, "- Component =", i, "- Total Length =", _, "- Total Edges =",
                      len(edges))

            for j in val:
                for k in val:
                    if j[1] != k[1]:
                        edges.add((j[1], k[1]))

            counter += 1

        end = datetime.now().time()

        if product_id is None:
            print("Start Time:", start, "End Time:", end)

            print("Writing layer 3 edges_normal to text file...")
            save_edges(edges)

            print("Process Successful! Total Edges =", len(edges))

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

            for i in ec:
                who_centrality[i[1]] = i[0]

            with open("l3_centrality.txt", 'wb') as fp:
                pickle.dump(who_centrality, fp)

            if product_id is None:
                save_ranks(ec)
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
