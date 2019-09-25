import pickle
from local_settings_netbeans import db

with db:
    cur = db.cursor()

    cur.execute("SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed where year(creation_ts) between 2002 and 2005")

    assignees = []
    for i in cur.fetchall():
        assignees.append(i[0])

    cur.execute("select assigned_to, bug_severity, count(*) from test_bugs_fixed_closed where year(creation_ts) between 2002 and 2005 "
                "group by assigned_to, bug_severity")

    assignee_severity_cnt = {}

    for i in cur.fetchall():
        if i[0] in assignees:
            if i[0] in assignee_severity_cnt:
                dic = assignee_severity_cnt[i[0]]
                dic[i[1]] = i[2]
                assignee_severity_cnt[i[0]] = dic
            else:
                assignee_severity_cnt[i[0]] = {i[1]: i[2]}

    print(assignee_severity_cnt)

    with open('assignee_severity_count.txt', 'wb') as fp:
        pickle.dump(assignee_severity_cnt, fp)

    print("Process Finished!")


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
