import pickle
from bs4 import BeautifulSoup
from local_settings_netbeans import db

not_downloaded_bugs = []
with db:
    print("Connected to db...")

    cur = db.cursor()

    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between 2001 and 2005")

    assignee_bug = {}
    for i in cur.fetchall():
        if i[1] in assignee_bug:
            lst = set(assignee_bug[i[1]])
            lst.add(i[0])
            assignee_bug[i[1]] = list(lst)
        else:
            assignee_bug[i[1]] = [i[0]]

    # print(len(assignee_bug))
    # print(assignee_bug)
    #
    # with open("assignee_bug.txt", 'wb') as fp:
    #     pickle.dump(assignee_bug, fp)

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

    print("Saving...")
    with open("assignee_reopened.txt", 'wb') as fp:
        pickle.dump(assignee_reopened_cnt, fp)

    print(assignee_reopened_cnt)

print("Process Complete!")
