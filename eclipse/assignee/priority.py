import pickle
from local_settings_eclipse import db

with db:
    cur = db.cursor()

    cur.execute(
        "SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed "
        "WHERE assigned_to IN (SELECT who FROM test_longdescs_fixed_closed)")

    assignees = []
    for i in cur.fetchall():
        assignees.append(i[0])

    cur.execute("select assigned_to, priority, count(*) from test_bugs_fixed_closed group by assigned_to, priority")

    assignee_priority_cnt = {}

    for i in cur.fetchall():
        if i[0] in assignees:
            if i[0] in assignee_priority_cnt:
                dic = assignee_priority_cnt[i[0]]
                dic[i[1]] = i[2]
                assignee_priority_cnt[i[0]] = dic
            else:
                assignee_priority_cnt[i[0]] = {i[1]: i[2]}

    print(assignee_priority_cnt)

<<<<<<< HEAD
    # with open('assignee_priority_count.txt', 'wb') as fp:
    #     pickle.dump(assignee_priority_cnt, fp)
=======
    with open('assignee_priority_count.txt', 'wb') as fp:
        pickle.dump(assignee_priority_cnt, fp)
>>>>>>> 847d6432758cc7a6c5721ab04a2aa8df1114db77

    print("Process Finished!")


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

