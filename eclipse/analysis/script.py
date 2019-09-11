import datetime
from itertools import permutations

import networkx as nx
import openpyxl

from local_settings_eclipse import db

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
            "select distinct who from test_longdescs_fixed_closed where bug_id in "
            "(select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6)".format(start, end))

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
                start) + " and " + str(end) + " and month(creation_ts) between 1 and 6")

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
        centrality = nx.eigenvector_centrality_numpy(graph)

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
            "select distinct who from test_longdescs_fixed_closed where bug_id in "
            "(select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6)".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6".format(
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
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6)".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, component_id, bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6".format(
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
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6)".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow reporter, bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6".format(
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
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6)".format(
                start, end))

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow op_sys, bug_id from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 1 and 6".format(
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
            "SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 7 and 12".format(
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
                        start = x[2]

                    if x[4] == 'FIXED':
                        end = x[2]
                        break

                if start is not None and end is not None:
                    tot_time.append(end - start)
                else:
                    try:
                        end = res[-1][2]
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
            "SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed WHERE assigned_to IN (SELECT who FROM test_longdescs_fixed_closed) and year(creation_ts) between {0} and {1} and month(creation_ts) between 7 and 12".format(
                start, end))

        assignees = []
        for i in cur.fetchall():
            assignees.append(i[0])

        cur.execute(
            "select assigned_to, priority, count(*) from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 7 and 12 group by assigned_to, priority".format(
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
            "SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed WHERE assigned_to IN (SELECT who FROM test_longdescs_fixed_closed) and year(creation_ts) between {0} and {1} and month(creation_ts) between 7 and 12".format(
                start, end))

        assignees = []
        for i in cur.fetchall():
            assignees.append(i[0])

        cur.execute(
            "select assigned_to, bug_severity, count(*) from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 7 and 12 group by assigned_to, bug_severity".format(
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
            "SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 7 and 12".format(
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
            "SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 7 and 12".format(
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
                        start = x[2]

                    if x[4] == 'CLOSED':
                        end = x[2]
                        break

                if start is not None and end is not None:
                    tot_time.append(end - start)
                else:
                    try:
                        end = res[-1][2]
                        tot_time.append(end - start)
                    except Exception:
                        pass

            sum_time = sum(tot_time, datetime.timedelta())
            hours = sum_time.days * 24 + sum_time.seconds * 0.000277778
            assignee_closed_time[i] = hours / len(temp_bugs)

            total -= 1

    return assignee_closed_time


def calculate_components(start, end):
    cur.execute("select assigned_to, count(distinct component_id) from test_bugs_fixed_closed where year(creation_ts) between {0} and {1} and month(creation_ts) between 7 and 12 group by assigned_to".format(start, end))

    assignee_comp = {}
    for i in cur.fetchall():
        if i[0] in assignees:
            assignee_comp[i[0]] = i[1]

    return assignee_comp


if __name__ == '__main__':
    wb = openpyxl.Workbook()
    sheet = wb.active

    titles = ['Assignee', 'L1', 'L2 - D1', 'L2 - D2', 'L3', 'L4', 'Avg Fixed', 'Avg Closed', 'Avg Reopened',
              'Total Components', 'Priority Points', 'Severity Points']

    sheet.append(titles)
    start = 2006
    end = 2006
    l1_centrality = layer_1(start, end)
    l2_d1_centrality = layer_2_d1(start, end)
    l2_d2_centrality = layer_2_d2(start, end)
    l3_centrality = layer_3(start, end)
    l4_centrality = layer_4(start, end)
    avg_fixed = calculate_avg_fixed(start, end)
    avg_closed = calculate_avg_closed(start, end)
    avg_reopened = calculate_reopened(start, end)
    components = calculate_components(start, end)
    priority = calculate_priority(start, end)
    severity = calculate_severity(start, end)

    for j in assignees:
        lst = []
        try:
            lst.append(j)
            lst.append(l1_centrality[j])
            lst.append(l2_d1_centrality[j])
            lst.append(l2_d2_centrality[j])
            lst.append(l3_centrality[j])
            lst.append(l4_centrality[j])
            lst.append(avg_fixed[j])
            lst.append(avg_closed[j])
            lst.append(avg_reopened[j])
            lst.append(components[j])
            lst.append(priority[j])
            lst.append(severity[j])

            print(lst)
            sheet.append(lst)
        except Exception:
            pass

    wb.save("analysis_" + str(start) + ".xlsx")

print("Finished!")
