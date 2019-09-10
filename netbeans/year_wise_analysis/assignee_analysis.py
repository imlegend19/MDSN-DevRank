import datetime

import openpyxl
from local_settings_eclipse import db

with db:
    cur = db.cursor()

    assignee = (13, 18, 35, 39, 47, 51, 53, 54, 238, 481, 2169, 2206, 2210, 2212, 2213, 2214, 2215, 2217, 2219,
                2220, 2224, 2225, 2227, 2228, 2231, 4861, 5892, 7084, 7311, 8707, 11674, 12825, 12828, 17212,
                21408, 60037, 66801)


def calculate_avg_fixed_time(start, end):
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between "
                + str(start) + " and " + str(end))

    assignee_bug = {}
    for b in cur.fetchall():
        if b[1] in assignee:
            if b[1] in assignee_bug:
                lst = set(assignee_bug[b[1]])
                lst.add(b[0])
                assignee_bug[b[1]] = list(lst)
            else:
                assignee_bug[b[1]] = [b[0]]

    bugs = set()
    for b in assignee_bug.values():
        for j in b:
            bugs.add(j)

    assignee_fixed_time = {}
    for i in assignee_bug:
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
                end = res[-1][2]
                tot_time.append(end - start)

        sum_time = sum(tot_time, datetime.timedelta())
        hours = sum_time.days * 24 + sum_time.seconds * 0.000277778
        assignee_fixed_time[i] = hours / len(temp_bugs)

    return assignee_fixed_time


def calculate_avg_closed_time(start, end):
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between "
                + str(start) + " and " + str(end))

    assignee_bug = {}
    for b in cur.fetchall():
        if b[1] in assignee:
            if b[1] in assignee_bug:
                lst = set(assignee_bug[b[1]])
                lst.add(b[0])
                assignee_bug[b[1]] = list(lst)
            else:
                assignee_bug[b[1]] = [b[0]]

    bugs = set()
    for b in assignee_bug.values():
        for j in b:
            bugs.add(j)

    assignee_closed_time = {}

    for i in assignee_bug:
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
                end = res[-1][2]
                tot_time.append(end - start)

        sum_time = sum(tot_time, datetime.timedelta())
        hours = sum_time.days * 24 + sum_time.seconds * 0.000277778
        assignee_closed_time[i] = hours / len(temp_bugs)

    return assignee_closed_time


def calculate_reopened_time(start, end):
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between "
                + str(start) + " and " + str(end))

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


def calculate_priority(start, end):
    cur.execute("select assigned_to, priority, count(*) from test_bugs_fixed_closed where year(creation_ts) between "
                + str(start) + " and " + str(end) + " group by assigned_to, priority")

    assignee_priority_cnt = {}

    for i in cur.fetchall():
        if i[0] in assignee:
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


def calculate_severity(start, end):
    cur.execute(
        "select assigned_to, bug_severity, count(*) from test_bugs_fixed_closed where year(creation_ts) "
        "between {0} and {1} group by assigned_to, bug_severity".format(
            str(start), str(end)))

    assignee_severity_cnt = {}

    for i in cur.fetchall():
        if i[0] in assignee:
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


if __name__ == '__main__':
    years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]

    wb = openpyxl.Workbook()
    sheet = wb.active

    titles = ['Year', 'Assignee', 'Avg Fixed Time', 'Avg Closed Time', 'Avg Reopened Time', "Priority Points",
              "Severity Points"]
    sheet.append(titles)

    for yr in years:
        print("Ongoing year " + str(yr))

        avg_fixed = calculate_avg_fixed_time(yr + 1, yr + 1)
        avg_closed = calculate_avg_closed_time(yr + 1, yr + 1)
        avg_reopened = calculate_reopened_time(yr + 1, yr + 1)
        priority_points = calculate_priority(yr + 1, yr + 1)
        severity_points = calculate_severity(yr + 1, yr + 1)

        for ass in assignee:
            val = ["Upto: " + str(yr), ass]
            try:
                val.append(avg_fixed[ass])
            except KeyError:
                val.append("")

            try:
                val.append(avg_closed[ass])
            except KeyError:
                val.append("")

            try:
                val.append(avg_reopened[ass])
            except KeyError:
                val.append("")

            try:
                val.append(priority_points[ass])
            except KeyError:
                val.append("")

            try:
                val.append(severity_points[ass])
            except KeyError:
                val.append("")

            sheet.append(val)

    wb.save("assignee_bug_analysis_2.xlsx")
    print("Finished!")
