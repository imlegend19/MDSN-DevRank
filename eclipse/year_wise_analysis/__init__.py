import datetime
from itertools import permutations

import openpyxl
from bs4 import BeautifulSoup
from dateutil import parser
from local_settings_eclipse import db

import networkx as nx

assignees = []
af_avg = {}
assignee_avg_fixed_time = {}
assignee_reopened_cnt = {}

with db:
    cur = db.cursor()
    cur.execute("select distinct assigned_to from bugs")

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
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts) between " + str(
                start) + " and " + str(end))

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
            "SELECT distinct bug_id FROM bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts) between " + str(
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


def layer_2_d1(year):
    with db:
        print("\tConnected to db!")
        cur = db.cursor()

        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from longdescs where bug_id in (select distinct bug_id from bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=" + str(
                year) + ")")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, bug_id from bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=" + str(
                year))
        product_bug = {}
        for i in cur.fetchall():
            if i[0] in product_bug.keys():
                val = product_bug[i[0]]
                val.add(i[1])
                product_bug[i[0]] = val
            else:
                product_bug[i[0]] = {i[1]}

        cur.execute("SELECT distinctrow bug_id, who from longdescs")
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
        print("\tConnected to db!")
        cur = db.cursor()

        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between " + str(
                start) + " and " + str(end) + ")")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, component_id, bug_id from bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts) between " + str(
                start) + " and " + str(end))

        prod_comp_bug = {}
        for i in cur.fetchall():
            if (i[0], i[1]) in prod_comp_bug.keys():
                val = prod_comp_bug[(i[0], i[1])]
                val.add(i[2])
                prod_comp_bug[(i[0], i[1])] = val
            else:
                prod_comp_bug[(i[0], i[1])] = {i[2]}

        cur.execute("SELECT distinctrow bug_id, who from longdescs")
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


def layer_3(year):
    with db:
        print("\tConnected to db!")
        cur = db.cursor()

        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from longdescs where bug_id in (select distinct bug_id from bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=" + str(
                year) + ")")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow reporter, bug_id from bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=" + str(
                year))

        reporter_bug = {}
        for i in cur.fetchall():
            if i[0] in reporter_bug.keys():
                val = reporter_bug[i[0]]
                val.add(i[1])
                reporter_bug[i[0]] = val
            else:
                reporter_bug[i[0]] = {i[1]}

        cur.execute("SELECT distinctrow bug_id, who from longdescs")
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
        print("\tConnected to db!")
        cur = db.cursor()

        print("\tFetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute(
            "select distinct who from test_longdescs_fixed_closed where bug_id in (select distinct bug_id from test_bugs_fixed_closed where year(creation_ts) between " + str(
                start) + " and " + str(end) + ")")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow op_sys, bug_id from bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts) between " + str(
                start) + " and " + str(end))

        os_bug = {}
        for i in cur.fetchall():
            if i[0] in os_bug.keys():
                val = os_bug[i[0]]
                val.add(i[1])
                os_bug[i[0]] = val
            else:
                os_bug[i[0]] = {i[1]}

        cur.execute("SELECT distinctrow bug_id, who from longdescs")
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


def calculate_avg_fixed(year):
    with db:
        af_avg.clear()
        assignee_avg_fixed_time.clear()
        assignee_reopened_cnt.clear()

        print("\tConnected to db...")
        cur = db.cursor()
        cur.execute(
            "SELECT DISTINCTROW bug_id, assigned_to FROM bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=" + str(
                year))

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

        assignee_fixed_time = {}
        assignee_first_fixed_time = {}

        main_cnt = len(bugs)
        for i in bugs:
            print("\tOngoing bug:", i, "Remaining :", main_cnt)
            main_cnt -= 1
            try:
                with open('bug_html/' + str(i) + '.html', 'r') as fp:
                    html = fp.read()

                soup = BeautifulSoup(html, features="html.parser")

                div = soup.find("div", attrs={"id": "bugzilla-body"})
                table = div.find("table")

                data = []
                for row in table.find_all("tr")[1:]:
                    dataset = list(td.get_text().replace("\n", "").strip() for td in row.find_all("td"))
                    data.append(dataset)

                if 'EST' in data[0][1]:
                    assigned_time = parser.parse(data[0][1], tzinfos={'EST': -5 * 3600})
                else:
                    assigned_time = parser.parse(data[0][1], tzinfos={'EDT': -5 * 3600})

                it = -1
                try:
                    while True:
                        if len(data[it]) == 5:
                            if 'CLOSED' in data[it]:
                                break
                            else:
                                it -= 1
                        elif len(data[it]) == 3:
                            if 'CLOSED' in data[it]:
                                it -= 1
                                while True:
                                    if len(data[it]) == 5:
                                        break
                                    else:
                                        it -= 1
                                break
                            else:
                                it -= 1

                    if 'EST' in data[it][1]:
                        finished_time = parser.parse(data[it][1], tzinfos={'EST': -5 * 3600})
                    else:
                        finished_time = parser.parse(data[it][1], tzinfos={'EDT': -5 * 3600})

                    assignee = None
                    for j in assignee_bug:
                        if i in assignee_bug[j]:
                            assignee = j
                            break

                    if assignee in assignee_fixed_time:
                        time = assignee_fixed_time[assignee][0] + (finished_time - assigned_time)
                        cnt = assignee_fixed_time[assignee][1] + 1

                        assignee_fixed_time[assignee] = [time, cnt]
                    else:
                        assignee_fixed_time[assignee] = [finished_time - assigned_time, 1]

                except IndexError:
                    pass

                for k in data:
                    if 'REOPENED' in k:
                        if assignee in assignee_reopened_cnt:
                            reopened = assignee_reopened_cnt[assignee][0]
                            tot = assignee_reopened_cnt[assignee][1]
                            assignee_reopened_cnt[assignee] = [reopened + 1, tot + 1]
                        else:
                            assignee_reopened_cnt[assignee] = [1, 1]
                    else:
                        if assignee in assignee_reopened_cnt:
                            reopened = assignee_reopened_cnt[assignee][0]
                            tot = assignee_reopened_cnt[assignee][1]
                            assignee_reopened_cnt[assignee] = [reopened, tot + 1]
                        else:
                            assignee_reopened_cnt[assignee] = [0, 1]

                if 'EST' in data[0][1]:
                    assigned_time = parser.parse(data[0][1], tzinfos={'EST': -5 * 3600})
                else:
                    assigned_time = parser.parse(data[0][1], tzinfos={'EDT': -5 * 3600})

                try:
                    for k in data:
                        if len(k) == 5:
                            if 'EST' in k[1]:
                                finished_time = parser.parse(k[1], tzinfos={'EST': -5 * 3600})
                            else:
                                finished_time = parser.parse(k[1], tzinfos={'EDT': -5 * 3600})
                        if 'CLOSED' in k:
                            if len(k) == 3:
                                break
                            else:
                                if 'EST' in k[1]:
                                    finished_time = parser.parse(k[1], tzinfos={'EST': -5 * 3600})
                                else:
                                    finished_time = parser.parse(k[1], tzinfos={'EDT': -5 * 3600})
                                break
                except Exception:
                    if len(data[-1]) == 3:
                        if 'EST' in data[-2][1]:
                            finished_time = parser.parse(data[-2][1], tzinfos={'EST': -5 * 3600})
                        else:
                            finished_time = parser.parse(data[-2][1], tzinfos={'EDT': -5 * 3600})
                    else:
                        if 'EST' in data[-1][1]:
                            finished_time = parser.parse(data[-1][1], tzinfos={'EST': -5 * 3600})
                        else:
                            finished_time = parser.parse(data[-1][1], tzinfos={'EDT': -5 * 3600})

                assignee = None
                for j in assignee_bug:
                    if i in assignee_bug[j]:
                        assignee = j
                        break

                if assignee in assignee_first_fixed_time:
                    time = assignee_first_fixed_time[assignee][0] + (finished_time - assigned_time)
                    cnt = assignee_first_fixed_time[assignee][1] + 1

                    assignee_first_fixed_time[assignee] = [time, cnt]
                else:
                    assignee_first_fixed_time[assignee] = [finished_time - assigned_time, 1]
            except Exception:
                pass

        for i in assignee_fixed_time:
            j = assignee_fixed_time[i]
            assignee_avg_fixed_time[i] = datetime.timedelta(seconds=((j[0].days * 86400 + j[0].seconds) / j[1]))

        for i in assignee_first_fixed_time:
            af_avg[i] = assignee_first_fixed_time[i][0] / assignee_first_fixed_time[i][1]


def calculate_priority(year):
    with db:
        cur = db.cursor()
        cur.execute(
            "SELECT DISTINCT assigned_to FROM bugs WHERE assigned_to IN (SELECT who FROM longdescs) and resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=" + str(
                year))

        assignees = []
        for i in cur.fetchall():
            assignees.append(i[0])

        cur.execute(
            "select assigned_to, priority, count(*) from bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=%d group by assigned_to, priority" % (
                year))
        assignee_priority_cnt = {}

        for i in cur.fetchall():
            if i[0] in assignees:
                if i[0] in assignee_priority_cnt:
                    dic = assignee_priority_cnt[i[0]]
                    dic[i[1]] = i[2]
                    assignee_priority_cnt[i[0]] = dic
                else:
                    assignee_priority_cnt[i[0]] = {i[1]: i[2]}

        return assignee_priority_cnt


def calculate_severity(year):
    with db:
        cur = db.cursor()
        cur.execute(
            "SELECT DISTINCT assigned_to FROM bugs WHERE assigned_to IN (SELECT who FROM longdescs) and resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=" + str(
                year))

        assignees = []
        for i in cur.fetchall():
            assignees.append(i[0])

        cur.execute(
            "select assigned_to, priority, count(*) from bugs where resolution='FIXED' and bug_status='CLOSED' and year(creation_ts)=%d group by assigned_to, priority" % (
                year))

        assignee_severity_cnt = {}

        for i in cur.fetchall():
            if i[0] in assignees:
                if i[0] in assignee_severity_cnt:
                    dic = assignee_severity_cnt[i[0]]
                    dic[i[1]] = i[2]
                    assignee_severity_cnt[i[0]] = dic
                else:
                    assignee_severity_cnt[i[0]] = {i[1]: i[2]}

        return assignee_severity_cnt


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


if __name__ == '__main__':
    years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]

    wb = openpyxl.Workbook()
    sheet = wb.active

    titles = ['Year', 'Assignee', 'L1', 'L2 - D1', 'L2 - D2', 'L3', 'L4', 'Avg Fixed', 'Re-open Count',
              'Avg First Fixed',
              'Priority', 'Severity']

    for i in years:
        print("Ongoing: " + str(i))
        l1_centrality = layer_1(2001, i)
        l2_d1_centrality = layer_2_d1(i)
        l2_d2_centrality = layer_2_d2(2001, i)
        l3_centrality = layer_3(i)
        l4_centrality = layer_4(2001, i)

        calculate_avg_fixed(i)

        priority = calculate_priority(i)
        severity = calculate_severity(i)

        for j in assignees:
            lst = []
            try:
                lst.append(i)
            except Exception:
                lst.append("null")

            try:
                lst.append(j)
            except Exception:
                lst.append("null")

            try:
                lst.append(l1_centrality[j])
            except Exception:
                lst.append("null")

            try:
                lst.append(l2_d1_centrality[j])
            except Exception:
                lst.append("null")

            try:
                lst.append(l2_d2_centrality[j])
            except Exception:
                lst.append("null")

            try:
                lst.append(l3_centrality[j])
            except Exception:
                lst.append("null")

            try:
                lst.append(l4_centrality[j])
            except Exception:
                lst.append("null")

            try:
                lst.append(assignee_avg_fixed_time[j])
            except Exception:
                lst.append("null")

            try:
                lst.append(assignee_reopened_cnt[j])
            except Exception:
                lst.append("null")

            try:
                lst.append(af_avg[j])
            except Exception:
                lst.append("null")

            try:
                lst.append(get_priority_points(priority[i]))
            except Exception:
                lst.append("null")

            try:
                lst.append(get_severity_points(severity[i]))
            except Exception:
                lst.append("null")

            sheet.append(lst)

    wb.save("analysis.xlsx")
    print("Finished!")
