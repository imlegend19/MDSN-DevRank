import datetime

import openpyxl
from bs4 import BeautifulSoup
from dateutil import parser

from local_settings_eclipse import db

with db:
    cur = db.cursor()
    cur.execute("select * from all_year_assignee")

    assignee = []
    for i in cur.fetchall():
        assignee.append(i[0])


def calculate_avg_fixed_time(start, end):
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between " + str(start) + " and " + str(end))

    assignee_bug = {}
    for i in cur.fetchall():
        if i[1] in assignee:
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
    main_cnt = len(bugs)

    for i in bugs:
        print("Ongoing bug:", i, "Remaining :", main_cnt)
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

                # print(dataset)

            # print(data)

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

                if ass in assignee_fixed_time:
                    time = assignee_fixed_time[ass][0] + (finished_time - assigned_time)
                    cnt = assignee_fixed_time[assignee][1] + 1

                    assignee_fixed_time[ass] = [time, cnt]
                else:
                    assignee_fixed_time[ass] = [finished_time - assigned_time, 1]

            except IndexError:
                pass
        except:
            pass

    assignee_avg_fixed_time = {}

    for i in assignee_fixed_time:
        j = assignee_fixed_time[i]
        assignee_avg_fixed_time[i] = datetime.timedelta(seconds=((j[0].days * 86400 + j[0].seconds) / j[1]))

    return assignee_avg_fixed_time


def calculate_reopened_time(start, end):
    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed")

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
    main_cnt = len(bugs)
    for i in bugs:
        print("Ongoing bug:", i, "Remaining :", main_cnt)
        main_cnt -= 1
        try:
            with open('bug_html/' + str(i) + '.html', 'r') as fp:
                html = fp.read()

            soup = BeautifulSoup(html, features="html.parser")

            div = soup.find("div", attrs={"id": "bugzilla-body"})
            table = div.find("table")

            headings = [th.get_text() for th in table.find("tr").find_all("th")]

            data = []
            for row in table.find_all("tr")[1:]:
                dataset = list(td.get_text().replace("\n", "").strip() for td in row.find_all("td"))
                data.append(dataset)

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
        except Exception:
            pass


if __name__ == '__main__':
    years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010]

    wb = openpyxl.Workbook()
    sheet = wb.active

    titles = ['Year', 'Avg Fixed Time', 'Avg Reopened Time']
    sheet.append(titles)

    for yr in years:
        val = []
        print("Ongoing year " + str(yr))

        val.append("Upto: " + str(yr))
        avg = calculate_avg_fixed_time(years[0], yr)

        for ass in assignee:
            try:
                val.append(avg[ass])
            except KeyError:
                val.append("")

        sheet.append(val)

    wb.save("analysis_.xlsx")
    print("Finished!")
