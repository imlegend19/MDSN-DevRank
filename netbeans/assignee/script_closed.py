import datetime
import pickle
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

    print(len(assignee_bug))
    print(assignee_bug)

    with open("assignee_bug.txt", 'wb') as fp:
        pickle.dump(assignee_bug, fp)

    bugs = set()
    for b in assignee_bug.values():
        for j in b:
            bugs.add(j)

    assignee_closed_time = {}
    total = len(assignee_bug)
    for i in assignee_bug:
        print("Remaining:", total)
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
                    start = x[3]

                if x[5] == 'CLOSED':
                    end = x[3]
                    break

            if start is not None and end is not None:
                tot_time.append(end - start)
            else:
                try:
                    end = res[-1][3]
                    tot_time.append(end - start)
                except Exception:
                    pass

        sum_time = sum(tot_time, datetime.timedelta())
        hours = sum_time.days * 24 + sum_time.seconds * 0.000277778
        assignee_closed_time[i] = hours / len(temp_bugs)

        total -= 1

    with open('assignee_closed_time.txt', 'wb') as fp:
        pickle.dump(assignee_closed_time, fp)

    # with open("assignee_reopened.txt", 'wb') as fp:
    #     pickle.dump(assignee_reopened_cnt, fp)
    #
    # af_avg = {}
    # for i in assignee_first_fixed_time:
    #     af_avg[i] = assignee_first_fixed_time[i][0] / assignee_first_fixed_time[i][1]
    #
    # with open('assignee_avg_first_fixed_time.txt', 'wb') as fp:
    #     pickle.dump(af_avg, fp)

print("Process Finished!")
