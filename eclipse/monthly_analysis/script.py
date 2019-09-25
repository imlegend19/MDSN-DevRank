import pickle
from itertools import permutations
import openpyxl
from local_settings_eclipse import db

l1e = None
l2_d1e = None
l2_d2e = None
l3e = None
l4e = None


def save_edges(edges, layer, year, phase, suffix):
    wb = openpyxl.Workbook()
    sheet = wb.active

    sheet.append(["Source", "Target"])

    for i in edges:
        sheet.append([i[0], i[1]])

    wb.save(str(year) + "/phase_" + str(phase) + "/layer" + str(layer) + suffix + "_" + str(year) + "_" + str(
            phase) + "_edges.xlsx")


def layer1(year, phase):
    global l1e

    if phase == 1:
        start = 1
        end = 6
    else:
        start = 7
        end = 12

    with db:
        print("Connected to db!")
        print("Fetching developers...")

        cur = db.cursor()

        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

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

        print("Fetching bugs from test_bug...")
        cur.execute("SELECT distinct bug_id FROM test_bugs_fixed_closed where year(creation_ts)=" + str(
            year) + " and month(creation_ts) between " + str(start) + " and " + str(end))

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

        l1e = edges
        save_edges(edges, 1, year, phase, "")


def layer2_d1(year, phase):
    global l2_d1e

    if phase == 1:
        start = 1
        end = 6
    else:
        start = 7
        end = 12

    with db:
        print("Connected to db!")
        cur = db.cursor()

        print("Fetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute("select distinct who from test_longdescs_fixed_closed")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute("SELECT distinctrow product_id, bug_id from test_bugs_fixed_closed where year(creation_ts)=" + str(
            year) + " and month(creation_ts) between " + str(start) + " and " + str(end))

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
            if i[1] in filtered_who:
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

        print("Setting up edges_normal...")
        edges = set()
        for i in product_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        l2_d1e = edges
        save_edges(edges, 2, year, phase, "_d1")


def layer2_d2(year, phase):
    global l2_d2e

    if phase == 1:
        start = 1
        end = 6
    else:
        start = 7
        end = 12

    with db:
        print("Connected to db!")
        cur = db.cursor()

        print("Fetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute("select distinct who from test_longdescs_fixed_closed")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute(
            "SELECT distinctrow product_id, component_id, bug_id from test_bugs_fixed_closed where year(creation_ts)=" + str(
                year) + " and month(creation_ts) between " + str(start) + " and " + str(end))

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
            if i[1] in filtered_who:
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

        print("Setting up edges_normal...")
        edges = set()
        for i in prod_comp_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        l2_d2e = edges
        save_edges(edges, 2, year, phase, "_d2")


def layer3(year, phase):
    global l3e

    if phase == 1:
        start = 1
        end = 6
    else:
        start = 7
        end = 12

    with db:
        print("Connected to db!")
        cur = db.cursor()

        print("Fetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute("select distinct who from test_longdescs_fixed_closed")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute("SELECT distinctrow reporter, bug_id from test_bugs_fixed_closed where year(creation_ts)=" + str(
            year) + " and month(creation_ts) between " + str(start) + " and " + str(end))

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
            if i[1] in filtered_who:
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

        print("Setting up edges_normal...")
        edges = set()
        for i in reporter_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        l3e = edges
        save_edges(edges, 3, year, phase, "")


def layer4(year, phase):
    global l4e

    if phase == 1:
        start = 1
        end = 6
    else:
        start = 7
        end = 12

    with db:
        print("Connected to db!")
        cur = db.cursor()

        print("Fetching developers...")
        cur.execute("SELECT who FROM who_commenting_on_more_than_10_bugs")

        dev = []
        for i in cur.fetchall():
            dev.append(i[0])

        cur.execute("select distinct who from test_longdescs_fixed_closed")

        filtered_who = []
        for i in cur.fetchall():
            filtered_who.append(i[0])

        cur.execute("SELECT distinctrow op_sys, bug_id from test_bugs_fixed_closed where year(creation_ts)=" + str(
            year) + " and month(creation_ts) between " + str(start) + " and " + str(end))

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
            if i[1] in filtered_who:
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

        print("Setting up edges_normal...")
        edges = set()
        for i in os_who.values():
            if len(list(i)) > 1:
                edg = list(permutations(list(i), 2))
                for j in edg:
                    if j[0] == j[1]:
                        print('err')
                    edges.add(j)

        l4e = edges
        save_edges(edges, 4, year, phase, "")


def combined(year, phase):
    edges = set(list(l1e) + list(l2_d1e) + list(l2_d2e) + list(l3e) + list(l4e))
    save_edges(edges, "combined", year, phase, "")

    print(len(edges))


if __name__ == '__main__':
    yr = 2004
    ph = 1

    layer1(yr, ph)
    layer2_d1(yr, ph)
    layer2_d2(yr, ph)
    layer3(yr, ph)
    layer4(yr, ph)
    combined(yr, ph)
