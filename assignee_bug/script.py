from urllib import request

from local_settings import db

with db:
    print("Connected to db...")

    cur = db.cursor()
    cur.execute("SELECT DISTINCT assigned_to FROM test_bug_fixed_closed")

    assignees = []
    for i in cur.fetchall():
        assignees.append(i[0].strip())

    print(assignees)
    cur.execute("SELECT DISTINCTROW who_id, who FROM test_comment_fixed_closed") \
 \
    who_id_who = {}
    for i in cur.fetchall():
        who_id_who[i[1].strip()] = i[0]

    print("Filtering assignee_bug...")
    segregated_assignees = {}
    for i in assignees:
        if i in who_id_who.keys():
            segregated_assignees[i] = who_id_who[i]

    print(segregated_assignees)
    print(len(segregated_assignees))

    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bug_fixed_closed")

    assignee_bug = {}
    for i in cur.fetchall():
        assignee_bug[i[1].strip()] = i[0]

    print(len(assignee_bug))

    for i in list(assignee_bug):
        if i not in segregated_assignees.keys():
            assignee_bug.pop(i)

    print(len(assignee_bug))

    # url = "https://bugzilla.gnome.org/show_activity.cgi?id="
    #
    # cnt = 1
    # for i in assignee_bug.values():
    #     print("Ongoing", cnt)
    #     request.urlretrieve(url + str(i), "bug_html/" + str(i) + ".html")
    #     cnt += 1
