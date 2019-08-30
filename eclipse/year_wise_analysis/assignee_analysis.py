import datetime

import openpyxl
<<<<<<< HEAD
=======
from bs4 import BeautifulSoup
from dateutil import parser

>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77
from local_settings_eclipse import db

# [13, 18, 35, 39, 47, 51, 53, 54, 238, 481, 2169, 2206, 2210, 2212, 2213, 2214, 2215, 2217, 2219, 2220, 2224, 2225,
# 2227, 2228, 2231, 4861, 5892, 7084, 7311, 8707, 11674, 12825, 12828, 17212, 21408, 60037, 66801]

with db:
    cur = db.cursor()
    cur.execute("select * from all_year_assignee")

    assignee = []
    for i in cur.fetchall():
        assignee.append(i[0])

    print(assignee)

assignee_names = {}


def calculate_avg_fixed_time(start, end):
<<<<<<< HEAD
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM bugs where year(creation_ts) between "
=======
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between "
>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77
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

    print(len(bugs))

    assignee_fixed_time = {}
    main_cnt = len(bugs)
    for b in bugs:
        print("Ongoing bug:", b, "Remaining :", main_cnt)
        main_cnt -= 1

        for j in assignee_bug:
            ass_bugs = assignee_bug[j]
            if b in ass_bugs:
                cur.execute("SELECT * FROM bugs_activity WHERE bug_id=" + str(b) + " order by bug_when")

                start = None
                end = None
                result = cur.fetchall()
                for k in result:
                    if start is None:
                        start = k[2]

                    if k[4].strip() == 'CLOSED' and k[5].strip() == 'VERIFIED':
                        end = k[2]

                if start is not None and end is not None:
                    if j in assignee_fixed_time:
                        time_count = assignee_fixed_time[j]
                        time_count[0] += (end - start)
                        time_count[1] += 1
                        assignee_fixed_time[j] = time_count
                    else:
                        assignee_fixed_time[j] = [(end - start), 1]
                elif start is not None and end is None:
                    end = result[-1][2]
                    if j in assignee_fixed_time:
                        time_count = assignee_fixed_time[j]
                        time_count[0] += (end - start)
                        time_count[1] += 1
                        assignee_fixed_time[j] = time_count
                    else:
                        assignee_fixed_time[j] = [(end - start), 1]

    assignee_avg_fixed_time = {}

    for b in assignee_fixed_time:
        j = assignee_fixed_time[b]
        assignee_avg_fixed_time[b] = datetime.timedelta(seconds=((j[0].days * 86400 + j[0].seconds) / j[1]))

    return assignee_avg_fixed_time


def calculate_reopened_time(start, end):
<<<<<<< HEAD
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM bugs where year(creation_ts) between "
=======
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between "
>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77
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
<<<<<<< HEAD
    # main_cnt = len(bugs)

    for b in bugs:
        # print("Ongoing bug:", b, "Remaining :", main_cnt)
        # main_cnt -= 1

        for j in assignee_bug:
            ass_bugs = assignee_bug[j]
            if b in ass_bugs:
                cur.execute("SELECT * FROM bugs_activity WHERE bug_id=" + str(j))

                reopened = False
                result = cur.fetchall()
                for k in result:
                    if 'REOPENED' in k:
                        reopened = True

                if reopened:
                    if j in assignee_reopened_cnt:
                        cnt_tot = assignee_reopened_cnt[j]
                        cnt_tot[0] += 1
                        cnt_tot[1] += 1
                        assignee_reopened_cnt[j] = cnt_tot
                    else:
                        assignee_reopened_cnt[j] = [1, 1]
                else:
                    if j in assignee_reopened_cnt:
                        cnt_tot = assignee_reopened_cnt[j]
                        cnt_tot[1] += 1
                        assignee_reopened_cnt[j] = cnt_tot
                    else:
                        assignee_reopened_cnt[j] = [0, 1]
=======
    for j in assignee_bug:
        ass_bugs = assignee_bug[j]
        if j in ass_bugs:
            cur.execute("SELECT * FROM bugs_activity WHERE bug_id=" + str(j))

            reopened = False
            result = cur.fetchall()
            for k in result:
                if 'REOPENED' in k:
                    reopened = True

            if reopened:
                if j in assignee_reopened_cnt:
                    cnt_tot = assignee_reopened_cnt[j]
                    cnt_tot[0] += 1
                    cnt_tot[1] += 1
                    assignee_reopened_cnt[j] = cnt_tot
                else:
                    assignee_reopened_cnt[j] = [1, 1]
            else:
                if j in assignee_reopened_cnt:
                    cnt_tot = assignee_reopened_cnt[j]
                    cnt_tot[1] += 1
                    assignee_reopened_cnt[j] = cnt_tot
                else:
                    assignee_reopened_cnt[j] = [0, 1]
>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77

    assignee_avg_reopened = {}

    for b in assignee_reopened_cnt:
        j = assignee_reopened_cnt[b]
        assignee_avg_reopened[b] = (j[0] / j[1]) * 100

    return assignee_avg_reopened


<<<<<<< HEAD
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
    cur.execute("select assigned_to, priority, count(*) from bugs where year(creation_ts) between "
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
        "select assigned_to, bug_severity, count(*) from bugs where year(creation_ts) "
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


=======
>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77
if __name__ == '__main__':
    years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]

    wb = openpyxl.Workbook()
    sheet = wb.active

<<<<<<< HEAD
    titles = ['Year', 'Assignee', 'Avg Fixed Time', 'Avg Reopened Time', "Priority Points", "Severity Points"]
=======
    titles = ['Year', 'Assignee', 'Avg Fixed Time', 'Avg Reopened Time']
>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77
    sheet.append(titles)

    for yr in years:
        if len(assignee_names.values()) == 20:
            break

        print("Ongoing year " + str(yr))

<<<<<<< HEAD
        avg = calculate_avg_fixed_time(2001, yr)
        avg_reopened = calculate_reopened_time(yr, yr)
        priority_points = calculate_priority(yr, yr)
        severity_points = calculate_severity(yr, yr)
=======
        avg = calculate_avg_fixed_time(yr, yr)
        avg_reopened = calculate_reopened_time(yr, yr)
>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77

        for ass in assignee:
            val = ["Upto: " + str(yr), ass]
            try:
                val.append(avg[ass])
            except KeyError:
                val.append("")

            try:
                val.append(avg_reopened[ass])
            except KeyError:
                val.append("")

<<<<<<< HEAD
            try:
                val.append(priority_points[ass])
            except KeyError:
                val.append("")

            try:
                val.append(severity_points[ass])
            except KeyError:
                val.append("")

=======
>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77
            sheet.append(val)

    wb.save("assignee_bug_analysis.xlsx")
    print("Finished!")

