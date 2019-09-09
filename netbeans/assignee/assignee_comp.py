import pickle
from local_settings_netbeans import db

with db:
    cur = db.cursor()
    cur.execute(
        "SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed "
        "WHERE assigned_to IN (SELECT who FROM test_longdescs_fixed_closed)")

    assignees = []
    for i in cur.fetchall():
        assignees.append(i[0])

    cur.execute("select assigned_to, count(distinct component_id) from test_bugs_fixed_closed "
                "group by assigned_to")

    assignee_comp = {}
    for i in cur.fetchall():
        if i[0] in assignees:
            assignee_comp[i[0]] = i[1]

    print(assignee_comp)
    with open('assignee_component.txt', 'wb') as fp:
        pickle.dump(assignee_comp, fp)

    print("Finished!")
