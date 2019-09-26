import datetime
import math
import pickle
from itertools import permutations

import networkx as nx
import openpyxl

from local_settings_netbeans import db

assignees = []
with db:
    cur = db.cursor()
    cur.execute("select distinct assigned_to from test_bugs_fixed_closed")

    for i in cur.fetchall():
        assignees.append(i[0])


def layer_1(start, end):
    with db:
        cur = db.cursor()
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        print("\tSetting up dict for who_id's who have commented on same bug...")
        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1})".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute("SELECT distinctrow bug_id, who from test_longdescs_fixed_closed")
        bug_who = {}
        bugs_taken = []
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
                bugs_taken.append(i[0])

        print("\tFetching bugs from test_bug...")
        cur.execute(
            "SELECT distinct bug_id FROM test_bugs_fixed_closed where year(creation_ts) between " + str(
                start) + " and " + str(end))

        bugs = []
        for i in cur.fetchall():
            bugs.append(i[0])

        print("\tFetched!")
        print("\tUpdating bug_who...")
        for i in list(bug_who.keys()):
            if i not in bugs:
                del bug_who[i]

        print("\tSetting up edges_normal...")
        edges = set()
        for i in bug_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        print("Total Edges :", len(edges))

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
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1})".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1}".format(
                start, end))
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

        print("Total Edges :", len(edges))

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
        print("\tConnected to db!")
        cur = db.cursor()

        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1})".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, component_id, bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1}".format(
                start, end))

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

        print("Total Edges :", len(edges))

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
        print("\tConnected to db!")
        cur = db.cursor()

        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1})".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow reporter, bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1}".format(
                start, end))

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

        print("Total Edges :", len(edges))

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
        print("\tConnected to db!")
        cur = db.cursor()

        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1})".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow op_sys, bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1}".format(
                start, end))

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

        print("Total Edges :", len(edges))

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


def calculate_avg_fixed(start, end):
    with db:
        print("\tConnected to db...")
        cur = db.cursor()
        cur.execute(
            "SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between {0} and {1}".format(
                start, end))

        assignee_bug = {}
        for i in cur.fetchall():
            if i[1] in assignee_bug:
                lst = set(assignee_bug[i[1]])
                lst.add(i[0])
                assignee_bug[i[1]] = list(lst)
            else:
                assignee_bug[i[1]] = [i[0]]

        print(len(assignee_bug))
        print(assignee_bug)

        bugs = set()
        for b in assignee_bug.values():
            for j in b:
                bugs.add(j)

        assignee_fixed_time = {}
        total = len(assignee_bug)
        for i in assignee_bug:
            print("Remaining:", total)
            # i: assignee
            tot_time = []
            temp_bugs = assignee_bug[i]
            for tb in temp_bugs:
                cur.execute("SELECT * FROM bugs_activity WHERE bug_id = {0}".format(tb))
                start = None
                end = None
                res = cur.fetchall()
                for x in res:
                    if start is None:
                        start = x[3]

                    if x[5] == 'FIXED':
                        end = x[3]
                        break

                if start is not None and end is not None:
                    tot_time.append(end - start)
                else:
                    try:
                        end = res[-1][3]
                        tot_time.append(end - start)
                    except Exception:
                        pass

            sum_time = sum(tot_time, datetime.timedelta())
            hours = sum_time.days * 24 + sum_time.seconds * 0.000277778
            assignee_fixed_time[i] = hours / len(temp_bugs)

            total -= 1

    return assignee_fixed_time


def calculate_priority(start, end):
    with db:
        cur = db.cursor()
        cur.execute(
            "SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed WHERE assigned_to IN (SELECT who FROM test_longdescs_fixed_closed) and year(creation_ts) between {0} and {1}".format(
                start, end))

        assignees = []
        for i in cur.fetchall():
            assignees.append(i[0])

        cur.execute(
            "select assigned_to, priority, count(*) from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} group by assigned_to, priority".format(
                start, end))

        assignee_priority_cnt = {}
        for i in cur.fetchall():
            if i[0] in assignees:
                if i[0] in assignee_priority_cnt:
                    dic = assignee_priority_cnt[i[0]]
                    dic[i[1]] = i[2]
                    assignee_priority_cnt[i[0]] = dic
                else:
                    assignee_priority_cnt[i[0]] = {i[1]: i[2]}

    assignee_priority_points = {}
    for i in assignee_priority_cnt:
        assignee_priority_points[i] = get_priority_points(assignee_priority_cnt[i])

    return assignee_priority_points


def calculate_severity(start, end):
    with db:
        cur = db.cursor()
        cur.execute(
            "SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed WHERE assigned_to IN (SELECT who FROM test_longdescs_fixed_closed) and year(creation_ts) between {0} and {1}".format(
                start, end))

        assignees = []
        for i in cur.fetchall():
            assignees.append(i[0])

        cur.execute(
            "select assigned_to, bug_severity, count(*) from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} group by assigned_to, bug_severity".format(
                start, end))

        assignee_severity_cnt = {}

        for i in cur.fetchall():
            if i[0] in assignees:
                if i[0] in assignee_severity_cnt:
                    dic = assignee_severity_cnt[i[0]]
                    dic[i[1]] = i[2]
                    assignee_severity_cnt[i[0]] = dic
                else:
                    assignee_severity_cnt[i[0]] = {i[1]: i[2]}

    assignee_severity_points = {}
    for i in assignee_severity_cnt:
        assignee_severity_points[i] = get_severity_points(assignee_severity_cnt[i])

    return assignee_severity_points


def get_priority_points(priority):
    points = 0
    for i in priority:
        if i == 'P1':
            points += priority[i]
        elif i == 'P2':
            points += priority[i] * 2
        elif i == 'P3':
            points += priority[i] * 3
        elif i == 'P4':
            points += priority[i] * 4
        else:
            points += priority[i] * 5

    return points


def get_severity_points(severity):
    points = 0
    for i in severity:
        if i == 'normal':
            points += severity[i] * 3
        elif i == 'critical':
            points += severity[i] * 5
        elif i == 'major':
            points += severity[i] * 4
        elif i == 'trivial':
            points += severity[i] * 1
        elif i == 'minor':
            points += severity[i] * 2
        elif i == 'blocker':
            points += severity[i] * 6

    return points


def calculate_reopened(start, end):
    with db:
        print("Connected to db...")

        cur = db.cursor()

        cur.execute(
            "SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between {0} and {1}".format(
                start, end))

        assignee_bug = {}
        for i in cur.fetchall():
            if i[1] in assignee_bug:
                lst = set(assignee_bug[i[1]])
                lst.add(i[0])
                assignee_bug[i[1]] = list(lst)
            else:
                assignee_bug[i[1]] = [i[0]]

        bugs = set()
        for i in assignee_bug.values():
            for j in i:
                bugs.add(j)

        assignee_reopened_cnt = {}
        # main_cnt = len(bugs)

        for i in assignee_bug:
            # i: assignee
            count = 0
            bugs = 0

            string = "("
            first = True
            for j in assignee_bug[i]:
                if first:
                    string += str(j)
                    first = False
                else:
                    string += ', '
                    string += str(j)
            string += ")"

            cur.execute("SELECT * FROM bugs_activity WHERE bug_id IN {0}".format(string))

            for j in cur.fetchall():
                if 'REOPENED' in j:
                    count += 1
                bugs += 1

            assignee_reopened_cnt[i] = [count, bugs]

        assignee_avg_reopened = {}

        for b in assignee_reopened_cnt:
            j = assignee_reopened_cnt[b]
            try:
                assignee_avg_reopened[b] = (j[0] / j[1]) * 100
            except ZeroDivisionError:
                assignee_avg_reopened[b] = 0

    return assignee_avg_reopened


def calculate_avg_closed(start, end):
    with db:
        print("\tConnected to db...")
        cur = db.cursor()
        cur.execute(
            "SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between {0} and {1}".format(
                start, end))

        assignee_bug = {}
        for i in cur.fetchall():
            if i[1] in assignee_bug:
                lst = set(assignee_bug[i[1]])
                lst.add(i[0])
                assignee_bug[i[1]] = list(lst)
            else:
                assignee_bug[i[1]] = [i[0]]

        print(len(assignee_bug))
        print(assignee_bug)

        bugs = set()
        for b in assignee_bug.values():
            for j in b:
                bugs.add(j)

        assignee_closed_time = {}
        total = len(assignee_bug)
        for i in assignee_bug:
            print("Remaining:", total)
            # i: assignee
            tot_time = []
            temp_bugs = assignee_bug[i]
            for tb in temp_bugs:
                cur.execute("SELECT * FROM bugs_activity WHERE bug_id = {0}".format(tb))
                start = None
                end = None
                res = cur.fetchall()
                for x in res:
                    if start is None:
                        start = x[3]

                    if x[5] == 'CLOSED':
                        end = x[3]
                        break

                if start is not None and end is not None:
                    tot_time.append(end - start)
                else:
                    try:
                        end = res[-1][3]
                        tot_time.append(end - start)
                    except Exception:
                        pass

            sum_time = sum(tot_time, datetime.timedelta())
            hours = sum_time.days * 24 + sum_time.seconds * 0.000277778
            assignee_closed_time[i] = hours / len(temp_bugs)

            total -= 1

    return assignee_closed_time


# and month(creation_ts) between 7 and 12
def calculate_components(start, end):
    cur.execute(
        "select assigned_to, count(distinct component_id) from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} "
        "group by assigned_to".format(start, end))

    assignee_comp = {}
    for i in cur.fetchall():
        if i[0] in assignees:
            assignee_comp[i[0]] = i[1]

    return assignee_comp


def calculate_entropy(edges, layer, other):
    graph = nx.DiGraph()
    graph.add_edges_from(edges)

    degrees = {}
    for (node, val) in graph.degree:
        degrees[node] = val

    entropy = {}
    total = len(list(graph.nodes))
    for i in graph.nodes:
        print("Remaining:", total)
        tot = sum(degrees.values())

        e1 = 0
        for j in graph.nodes:
            pi = degrees[j] / tot
            e1 += pi * math.log(pi, 10)

        e1 = -e1

        graph2 = nx.DiGraph()
        graph2.add_edges_from(edges)
        graph2.remove_node(i)

        e2 = 0
        deg = {}
        for (node, val) in graph2.degree:
            deg[node] = val

        for j in graph2.nodes:
            pi = deg[j] / tot
            try:
                e2 += pi * math.log(pi, 10)
            except Exception:
                pass

        e2 = -e2
        entropy[i] = e2 - e1
        total -= 1

    if layer is None:
        with open("entropy_comb.txt", 'wb') as fp:
            pickle.dump(entropy, fp)
    else:
        if not other:
            with open("layer" + str(layer) + "_entropy.txt", 'wb') as fp:
                pickle.dump(entropy, fp)
        else:
            with open("layer" + str(layer) + "_d2" + "_entropy.txt", 'wb') as fp:
                pickle.dump(entropy, fp)

    return entropy


def get_bets_file(layer, end):
    p = '/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/gephi_analysis/'
    with open(p + "betweenness/betweenness_layer_" + str(layer) + end + ".txt", 'rb') as fp:
        c = pickle.load(fp)

    return c


def get_eg_file(layer, end):
    p = '/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/gephi_analysis/'
    with open(p + "eigenvector/eigenvector_layer_" + str(layer) + end + ".txt", 'rb') as fp:
        c = pickle.load(fp)

    return c


def get_cl_file(layer, end):
    p = '/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/gephi_analysis/'
    with open(p + "closeness/closeness_layer_" + str(layer) + end + ".txt", 'rb') as fp:
        c = pickle.load(fp)

    return c


def get_deg_file(layer, end):
    p = '/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/gephi_analysis/'
    with open(p + "degree/degree_layer_" + str(layer) + end + ".txt", 'rb') as fp:
        c = pickle.load(fp)

    return c


def get_hc_file(layer, end):
    p = '/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/gephi_analysis/'
    with open(p + "harmonic_closeness/harmonic_closeness_layer_" + str(layer) + end + ".txt", 'rb') as fp:
        c = pickle.load(fp)

    return c


def get_pg_file(layer, end):
    p = '/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/gephi_analysis/'
    with open(p + "pagerank/pagerank_layer_" + str(layer) + end + ".txt", 'rb') as fp:
        c = pickle.load(fp)

    return c


def get_entropy(layer, end, is_comb):
    if not is_comb:
        with open("layer" + str(layer) + end + "_entropy" + ".txt", 'rb') as fp:
            c = pickle.load(fp)
    else:
        with open("entropy_comb" + ".txt", 'rb') as fp:
            c = pickle.load(fp)

    return c


def get_edges(layer, definition):
    if definition == 'comb':
        with open('/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/edges_comb.txt', 'rb') as fp:
            edges = list(pickle.load(fp))

        return edges
    else:
        with open('/home/niit1/PycharmProjects/Data-Mining-Research/eclipse/edges/definition_' + str(definition) + '/layer' + str(layer) + '_edges_fc.txt', 'rb') as fp:
            edges = list(pickle.load(fp))

        return edges


if __name__ == '__main__':
    wb = openpyxl.Workbook()
    sheet = wb.active

    titles = ['Assignee', 'L1', 'L2 - D1', 'L2 - D2', 'L3', 'L4', 'Combined', 'Avg Fixed', 'Avg Closed', 'Avg Reopened',
              'Total Components', 'Priority Points', 'Severity Points', 'Bet-L1', 'Bet-L2-D1', 'Bet-L2-D2', 'Bet-L3',
              'Bet-L4', 'Bet-Comb', 'Close-L1', 'Close-L2-D1', 'Close-L2-D2', 'Close-L3', 'Close-L4', 'Close-Comb',
              'H-Close-L1', 'H-Close-L2-D1', 'H-Close-L2-D2', 'H-Close-L3', 'H-Close-L4', 'H-Close-Comb', 'Page-L1',
              'Page-L2-D1', 'Page-L2-D2', 'Page-L3', 'Page-L4', 'Page-Comb', 'Deg-L1', 'Deg-L2-D1', 'Deg-L2-D2',
              'Deg-L3', 'Deg-L4', 'Deg-Comb', 'Ent-L1', 'Ent-L2-D1', 'Ent-L2-D2', 'Ent-L3', 'Ent-L4', 'Ent-Comb']

    start = 2001
    end = 2005

    sheet.append(titles)
    l1_centrality = get_eg_file(1, "")
    l2_d1_centrality = get_eg_file(2, "_d1")
    l2_d2_centrality = get_eg_file(2, "_d2")
    l3_centrality = get_eg_file(3, "")
    l4_centrality = get_eg_file(4, "")
    comb = get_eg_file("", "combined")
    avg_fixed = calculate_avg_fixed(start, end)
    avg_closed = calculate_avg_closed(start, end)
    avg_reopened = calculate_reopened(start, end)
    components = calculate_components(start, end)
    priority = calculate_priority(start, end)
    severity = calculate_severity(start, end)
    bet_l1 = get_bets_file(1, "")
    bet_l2_d1 = get_bets_file(2, "_d1")
    bet_l2_d2 = get_bets_file(2, "_d2")
    bet_l3 = get_bets_file(3, "")
    bet_l4 = get_bets_file(4, "")
    bet_comb = get_bets_file("combined", "")
    cl_l1 = get_cl_file(1, "")
    cl_l2_d1 = get_cl_file(2, "_d1")
    cl_l2_d2 = get_cl_file(2, "_d2")
    cl_l3 = get_cl_file(3, "")
    cl_l4 = get_cl_file(4, "")
    cl_comb = get_cl_file("combined", "")
    hcl_l1 = get_hc_file(1, "")
    hcl_l2_d1 = get_hc_file(2, "_d1")
    hcl_l2_d2 = get_hc_file(2, "_d2")
    hcl_l3 = get_hc_file(3, "")
    hcl_l4 = get_hc_file(4, "")
    hcl_comb = get_hc_file("combined", "")
    pg_l1 = get_pg_file(1, "")
    pg_l2_d1 = get_pg_file(2, "_d1")
    pg_l2_d2 = get_pg_file(2, "_d2")
    pg_l3 = get_pg_file(3, "")
    pg_l4 = get_pg_file(4, "")
    pg_comb = get_pg_file("combined", "")
    deg_l1 = get_deg_file(1, "")
    deg_l2_d1 = get_deg_file(2, "_d1")
    deg_l2_d2 = get_deg_file(2, "_d2")
    deg_l3 = get_deg_file(3, "")
    deg_l4 = get_deg_file(4, "")
    deg_comb = get_deg_file("combined", '')
    ent_l1 = calculate_entropy(get_edges(1, 1), 1, False)
    ent_l2_d1 = calculate_entropy(get_edges(2, 1), 2, False)
    ent_l2_d2 = calculate_entropy(get_edges(2, 2), 2, True)
    ent_l3 = calculate_entropy(get_edges(3, 1), 3, False)
    ent_l4 = calculate_entropy(get_edges(4, 1), 4, False)
    ent_comb = calculate_entropy(get_edges(1, 'comb'), None, False)

    for j in assignees:
        lst = []
        try:
            lst.append(j)
            lst.append(l1_centrality[j])
            lst.append(l2_d1_centrality[j])
            lst.append(l2_d2_centrality[j])
            lst.append(l3_centrality[j])
            lst.append(l4_centrality[j])
            lst.append(comb[j])
            lst.append(avg_fixed[j])
            lst.append(avg_closed[j])
            lst.append(avg_reopened[j])
            lst.append(components[j])
            lst.append(priority[j])
            lst.append(severity[j])
            lst.append(bet_l1[j])
            lst.append(bet_l2_d1[j])
            lst.append(bet_l2_d2[j])
            lst.append(bet_l3[j])
            lst.append(bet_l4[j])
            lst.append(bet_comb[j])
            lst.append(cl_l1[j])
            lst.append(cl_l2_d1[j])
            lst.append(cl_l2_d2[j])
            lst.append(cl_l3[j])
            lst.append(cl_l4[j])
            lst.append(cl_comb[j])
            lst.append(hcl_l1[j])
            lst.append(hcl_l2_d1[j])
            lst.append(hcl_l2_d2[j])
            lst.append(hcl_l3[j])
            lst.append(hcl_l4[j])
            lst.append(hcl_comb[j])
            lst.append(pg_l1[j])
            lst.append(pg_l2_d1[j])
            lst.append(pg_l2_d2[j])
            lst.append(pg_l3[j])
            lst.append(pg_l4[j])
            lst.append(pg_comb[j])
            lst.append(deg_l1[j])
            lst.append(deg_l2_d1[j])
            lst.append(deg_l2_d2[j])
            lst.append(deg_l3[j])
            lst.append(deg_l4[j])
            lst.append(deg_comb[j])
            lst.append(ent_l1[j])
            lst.append(ent_l2_d1[j])
            lst.append(ent_l2_d2[j])
            lst.append(ent_l3[j])
            lst.append(ent_l4[j])
            lst.append(ent_comb[j])

            print(lst)
            sheet.append(lst)
        except Exception:
            pass

    wb.save("analysis_" + str(start) + "_" + str(end) + "_gephi" + ".xlsx")

print("Finished!")
