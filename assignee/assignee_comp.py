import pickle

from local_settings import db

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

    cur.execute("select assigned_to, count(distinct component) from test_bug_fixed_closed "
                "group by assigned_to")

    assignee_comp = {}
    for i in cur.fetchall():
        if i[0].strip() in segregated_assignees:
            assignee_comp[segregated_assignees[i[0].strip()]] = i[1]

    print(assignee_comp)
    with open('assignee_component.txt', 'wb') as fp:
        pickle.dump(assignee_comp, fp)

    print("Finished!")
