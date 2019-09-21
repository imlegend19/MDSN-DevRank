import pickle
from itertools import permutations

import openpyxl
import networkx as nx
from local_settings_eclipse import db

"""
Layer 1 Network: 

Edge between developers who commented on same bug.

Dataset Used : eclipse
Table : test_bugs_fixed_closed, test_longdescs_fixed_closed
"""


def save_edges(edges):
    with open('layer1_edges_fc.txt', 'wb') as file:
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
    wb.save("layer1_ranks_fc.xlsx")


def layer1(product_id):
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
            print("Setting up dict for who_id's who have commented on same bug...")

        cur.execute("select distinct who from test_longdescs_fixed_closed")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute("SELECT distinctrow bug_id, who from test_longdescs_fixed_closed")
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

        # with open("bugs_taken.txt", 'wb') as fp:
        #     pickle.dump(bugs_taken, fp)

        print("Fetching bugs from test_bug...")
        cur.execute("SELECT distinct bug_id FROM test_bugs_fixed_closed")

        bugs = []
        for i in cur.fetchall():
            bugs.append(i[0])

        print("Fetched!")
        print("Updating bug_who...")

        for i in list(bug_who.keys()):
            if i not in bugs:
                del bug_who[i]

        print("Setting up edges_normal...")

        edges = set()
        for i in bug_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        # save_edges(edges)
        print("Saved edges_normal! Total edges_normal:", len(edges))

        graph = nx.DiGraph()
        graph.add_edges_from(list(edges))

        neighbours = {}
        for i in list(graph.nodes):
            lst = list(graph.neighbors(i))
            neighbours[i] = lst

        print(neighbours)

        path = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/neighbours/definition_1/"
        with open(path + "layer_1_neighbours.txt", 'wb') as fp:
            pickle.dump(neighbours, fp)

        path = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/neighbours/definition_2/"
        with open(path + "layer_1_neighbours.txt", 'wb') as fp:
            pickle.dump(neighbours, fp)

        # degrees = {}
        # for (node, val) in graph.degree:
        #     degrees[node] = val
        #
        # print(degrees)
        #
        # path = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/degree_centrality/definition_2/"
        # with open(path + "layer_1_degree.txt", 'wb') as fp:
        #     pickle.dump(degrees, fp)

        # print("Calculating eigenvector centrality...")
        # centrality = nx.eigenvector_centrality(graph)
        #
        # ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
        # ec.reverse()
        #
        # who_centrality = {}
        #
        # for i in ec:
        #     who_centrality[i[1]] = i[0]
        #
        # with open("l1_centrality.txt", 'wb') as fp:
        #     pickle.dump(who_centrality, fp)
        #
        # save_ranks(ec)

        print("Process Competed!")


layer1(None)
