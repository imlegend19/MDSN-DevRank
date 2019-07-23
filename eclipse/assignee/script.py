import pickle
from urllib import request

from local_settings_eclipse import db
from bs4 import BeautifulSoup
from dateutil import parser

not_downloaded_bugs = []
with db:
    print("Connected to db...")

    cur = db.cursor()

    cur.execute("SELECT DISTINCTROW bug_id, assigned_to FROM test_bugs_fixed_closed")

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

    print(len(assignee_bug))

    url = "https://bugs.eclipse.org/bugs/show_activity.cgi?id="

    bugs = set()
    for i in assignee_bug.values():
        for j in i:
              bugs.add(j)

cnt = len(bugs)
for i in bugs:
    try:
        print("Remaining", cnt)
        request.urlretrieve(url + str(i), "bug_html/" + str(i) + ".html")

    except:
        url_not_downloaded=url + str(i)
        not_downloaded_bugs.append(url_not_downloaded)
        print(not_downloaded_bugs)
    cnt -= 1


with open("not_downloaded_bugs.txt",'wb') as fp:
    pickle.dump(not_downloaded_bugs,fp)

print("Process Finished!")
