from itertools import permutations
import openpyxl
from local_settings_eclipse import db

import networkx as nx

assignees = []
af_avg = {}
assignee_avg_fixed_time = {}
assignee_reopened_cnt = {}

with db:
    cur = db.cursor()
    cur.execute("select * from all_year_assignee")

    for i in cur.fetchall():
        assignees.append(i[0])


def layer_1(start, end):
    with db:
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for dv in cur.fetchall():
            dev.append(dv[0])

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

        print("\tFetching bugs from test_bug...")
        cur.execute("SELECT distinct bug_id FROM test_bugs_fixed_closed where year(creation_ts) between " + str(
            start) + " and " + str(end))

        bugs = []
        for i in cur.fetchall():
            bugs.append(i[0])

        for i in list(bug_who.keys()):
            if i not in bugs:
                del bug_who[i]

        print("\tSetting up edges...")
        edges = set()
        for dv in bug_who.values():
            if len(list(dv)) > 1:
                edg = list(permutations(list(dv), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        graph = nx.DiGraph()
        graph.add_edges_from(list(edges))

        print("\tCalculating eigenvector centrality...")
        centrality = nx.eigenvector_centrality(graph)

        ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
        ec.reverse()

        who_centrality = {}
        for dv in ec:
            who_centrality[dv[1]] = dv[0]

        return who_centrality


def layer_2_d1(start, end):
    with db:
        print("\tConnected to db!")
        cur = db.cursor()

        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in "
            "(select distinct bug_id from test_bugs_fixed_closed where year("
            "creation_ts) between " + str(start) + " and " + str(end) + ")")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, bug_id from test_bugs_fixed_closed where year(creation_ts) between " + str(
                start) + " and " + str(end))

        product_bug = {}
        for i in cur.fetchall():
            if i[0] in product_bug.keys():
                val = product_bug[i[0]]
                val.add(i[1])
                product_bug[i[0]] = val
            else:
                product_bug[i[0]] = {i[1]}

        cur.execute("SELECT distinctrow bug_id, who from test_longdescs_fixed_closed")
        bug_who = {}
        for i in cur.fetchall():
            if i[1] in filtered_who and i[1] in assignees:
                if i[0] in bug_who.keys():
                    if i[1] in dev:
                        val = bug_who[i[0]]
                        val.add(i[1])
                        bug_who[i[0]] = val
                else:
                    if i[1] in dev:
                        bug_who[i[0]] = {i[1]}

        product_who = {}
        for i in product_bug:
            val = product_bug[i]
            who_s = set()
            for j in val:
                try:
                    for k in bug_who[j]:
                        who_s.add(k)
                except KeyError:
                    pass

            product_who[i] = who_s

        print("\tSetting up edges_normal...")
        edges = set()
        for i in product_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        graph = nx.DiGraph()
        graph.add_edges_from(list(edges))

        print("\tCalculating eigenvector centrality...")
        centrality = nx.eigenvector_centrality(graph)

        ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
        ec.reverse()

        who_centrality = {}

        for i in ec:
            who_centrality[i[1]] = i[0]

        return who_centrality


def layer_2_d2(start, end):
    with db:
        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id "
            "from test_bugs_fixed_closed where year(creation_ts) between " + str(start) + " and " + str(end) + ")")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, component_id, bug_id from test_bugs_fixed_closed where "
            "year(creation_ts) between " + str(start) + " and " + str(end))

        prod_comp_bug = {}
        for i in cur.fetchall():
            if (i[0], i[1]) in prod_comp_bug.keys():
                val = prod_comp_bug[(i[0], i[1])]
                val.add(i[2])
                prod_comp_bug[(i[0], i[1])] = val
            else:
                prod_comp_bug[(i[0], i[1])] = {i[2]}

        cur.execute("SELECT distinctrow bug_id, who from test_longdescs_fixed_closed")
        bug_who = {}
        for i in cur.fetchall():
            if i[1] in filtered_who and i[1] in assignees:
                if i[0] in bug_who.keys():
                    if i[1] in dev:
                        val = bug_who[i[0]]
                        val.add(i[1])
                        bug_who[i[0]] = val
                else:
                    if i[1] in dev:
                        bug_who[i[0]] = {i[1]}

        prod_comp_who = {}
        for i in prod_comp_bug:
            val = prod_comp_bug[i]
            who_s = set()
            for j in val:
                try:
                    for k in bug_who[j]:
                        who_s.add(k)
                except KeyError:
                    pass

            prod_comp_who[i] = who_s

        print("\tSetting up edges_normal...")
        edges = set()
        for i in prod_comp_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        graph = nx.DiGraph()
        graph.add_edges_from(list(edges))

        print("\tCalculating eigenvector centrality...")
        centrality = nx.eigenvector_centrality(graph)

        ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
        ec.reverse()

        who_centrality = {}
        for i in ec:
            who_centrality[i[1]] = i[0]

        return who_centrality


def layer_3(start, end):
    with db:
        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in "
            "(select distinct bug_id from test_bugs_fixed_closed where "
            "year(creation_ts) between " + str(start) + " and " + str(end) + ")")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow reporter, bug_id from test_bugs_fixed_closed where year(creation_ts) between "
            + str(start) + " and " + str(end))

        reporter_bug = {}
        for i in cur.fetchall():
            if i[0] in reporter_bug.keys():
                val = reporter_bug[i[0]]
                val.add(i[1])
                reporter_bug[i[0]] = val
            else:
                reporter_bug[i[0]] = {i[1]}

        cur.execute("SELECT distinctrow bug_id, who from test_longdescs_fixed_closed")
        bug_who = {}
        for i in cur.fetchall():
            if i[1] in filtered_who and i[1] in assignees:
                if i[0] in bug_who.keys():
                    if i[1] in dev:
                        val = bug_who[i[0]]
                        val.add(i[1])
                        bug_who[i[0]] = val
                else:
                    if i[1] in dev:
                        bug_who[i[0]] = {i[1]}

        reporter_who = {}
        for i in reporter_bug:
            val = reporter_bug[i]
            who_s = set()
            for j in val:
                try:
                    for k in bug_who[j]:
                        who_s.add(k)
                except KeyError:
                    pass

            reporter_who[i] = who_s

        print("\tSetting up edges_normal...")
        edges = set()
        for i in reporter_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        graph = nx.DiGraph()
        graph.add_edges_from(list(edges))

        print("\tCalculating eigenvector centrality...")
        centrality = nx.eigenvector_centrality(graph)

        ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
        ec.reverse()

        who_centrality = {}
        for i in ec:
            who_centrality[i[1]] = i[0]

        return who_centrality


def layer_4(start, end):
    with db:
        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from "
            "test_bugs_fixed_closed where year(creation_ts) between " + str(start) + " and " + str(end) + ")")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow op_sys, bug_id from test_bugs_fixed_closed where year(creation_ts) between "
            + str(start) + " and " + str(end))

        os_bug = {}
        for i in cur.fetchall():
            if i[0] in os_bug.keys():
                val = os_bug[i[0]]
                val.add(i[1])
                os_bug[i[0]] = val
            else:
                os_bug[i[0]] = {i[1]}

        cur.execute("SELECT distinctrow bug_id, who from test_longdescs_fixed_closed")
        bug_who = {}
        for i in cur.fetchall():
            if i[1] in filtered_who and i[1] in assignees:
                if i[0] in bug_who.keys():
                    if i[1] in dev:
                        val = bug_who[i[0]]
                        val.add(i[1])
                        bug_who[i[0]] = val
                else:
                    if i[1] in dev:
                        bug_who[i[0]] = {i[1]}

        os_who = {}
        for i in os_bug:
            val = os_bug[i]
            who_s = set()
            for j in val:
                try:
                    for k in bug_who[j]:
                        who_s.add(k)
                except KeyError:
                    pass

            os_who[i] = who_s

        print("\tSetting up edges_normal...")
        edges = set()
        for i in os_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        graph = nx.DiGraph()
        graph.add_edges_from(list(edges))

        print("\tCalculating eigenvector centrality...")
        centrality = nx.eigenvector_centrality(graph)

        ec = sorted(('{:0.5f}'.format(c), v) for v, c in centrality.items())
        ec.reverse()

        who_centrality = {}

        for i in ec:
            who_centrality[i[1]] = i[0]

        return who_centrality


if __name__ == '__main__':
    years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]

    wb = openpyxl.Workbook()
    sheet = wb.active

    titles = ['Year', 'Assignee', 'L1', 'L2 - D1', 'L2 - D2', 'L3', 'L4']
    sheet.append(titles)

    for yr in years:
        print("Ongoing year " + str(yr))

        l1 = layer_1(years[0], yr)
        l2_d1 = layer_2_d1(years[0], yr)
        l2_d2 = layer_2_d2(years[0], yr)
        l3 = layer_3(years[0], yr)
        l4 = layer_4(years[0], yr)

        for ass in assignees:
            row = []
            if yr == 2001:
                row.append(2001)
            else:
                row.append("Upto " + str(yr))

            row.append(ass)

            try:
                row.append(l1[ass])
            except KeyError:
                row.append("")

            try:
                row.append(l2_d1[ass])
            except KeyError:
                row.append("")

            try:
                row.append(l3[ass])
            except KeyError:
                row.append("")

            try:
                row.append(l4[ass])
            except KeyError:
                row.append("")

            sheet.append(row)

    wb.save("analysis.xlsx")
    print("Finished!")
