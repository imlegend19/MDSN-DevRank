import os.path
from local_settings_eclipse import db
from urllib import request

with db:
    cur = db.cursor()
    cur.execute("SELECT DISTINCT bug_id FROM test_bugs_fixed_closed")

    url = "https://bugs.eclipse.org/bugs/show_activity.cgi?id="

    bugs = []
    for i in cur.fetchall():
        if os.path.isfile("bug_html/" + str(i[0]) + ".html"):
            print("Yes")
        else:
            request.urlretrieve(url + str(i), "bug_html/" + str(i) + ".html")
