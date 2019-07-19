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


def save_edges(edges):
    with open('layer1_edges_fc.txt', 'wb') as file:
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
    wb.save("layer1_ranks_fc.xlsx")


def layer1(product_id):
    with db:
        if product_id is None:
            print("Connected to db!")
            print("Fetching developers...")

        cur = db.cursor()

        cur.execute("SELECT DISTINCT who_id FROM who_ids_commenting_on_more_than_10_bugs")
        dev = []

        for i in cur.fetchall():
            dev.append(i[0])

        bug_who = {}

        if product_id is None:
            print("Setting up dict for who_id's who have commented on same bug...")

        cur.execute("SELECT distinctrow bug_id, who_id FROM test_comment_fixed_closed")

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

        if product_id is None:
            print("Fetching bugs from test_bug...")
            cur.execute("SELECT distinct bug_id FROM test_bug_fixed_closed")
        else:
            cur.execute("SELECT distinct bug_id FROM test_bug_fixed_closed WHERE product_id=" + str(product_id))

        bugs = []
        for i in cur.fetchall():
            bugs.append(i[0])

        if product_id is None:
            print("Fetched!")
            print("Updating bug_who...")

        for i in list(bug_who.keys()):
            if i not in bugs:
                del bug_who[i]

        if product_id is None:
            print("Setting up edges...")

        edges = set()
        for i in bug_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    edges.add(j)

        # if product_id is None:
        #     save_edges(edges)
        #     print("Saved edges! Total edges:", len(edges))

        graph = nx.DiGraph()
        graph.add_edges_from(list(edges))

        if product_id is None:
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

            # save_ranks(developer, ec)
        else:
            sum_ec = 0

            for i in ec:
                sum_ec += float(i[0])

            avg_centrality = sum_ec / len(ec)
            # print(product_id, ' : ', avg_centrality)

            return avg_centrality

        if product_id is None:
            print("Process Competed!")


layer1(None)
