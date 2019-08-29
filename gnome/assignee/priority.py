import pickle
from local_settings_gnome import db

with db:
    cur = db.cursor()

    with open("assignee_who.txt", 'rb') as fp:
        assignee_who = pickle.load(fp)

    cur.execute("SELECT DISTINCT assigned_to FROM test_bug_fixed_closed")

    assignees = []
    for i in cur.fetchall():
        assignees.append(i[0].strip())

    print(assignees)
    cur.execute("SELECT DISTINCTROW who_id, who FROM test_comment_fixed_closed")
    who_id_who = {}
    for i in cur.fetchall():
        who_id_who[i[1].strip()] = i[0]

    no_comment_assignee = []

    print("Filtering assignee...")
    segregated_assignees = {}
    for i in assignees:
        if i in who_id_who.keys():
            segregated_assignees[i] = who_id_who[i]
        else:
            no_comment_assignee.append(i)

    cur.execute("select assigned_to, priority, count(*) from test_bug_fixed_closed group by assigned_to, priority")

    assignee_priority_cnt = {}

    for i in cur.fetchall():
        if i[0].strip() in segregated_assignees:
            if segregated_assignees[i[0].strip()] in assignee_priority_cnt:
                dic = assignee_priority_cnt[segregated_assignees[i[0].strip()]]
                dic[i[1]] = i[2]
                assignee_priority_cnt[segregated_assignees[i[0].strip()]] = dic
            else:
                assignee_priority_cnt[segregated_assignees[i[0].strip()]] = {i[1]: i[2]}

    print(assignee_priority_cnt)

    with open('assignee_priority_count.txt', 'wb') as fp:
        pickle.dump(assignee_priority_cnt, fp)

    print("Process Finished!")
