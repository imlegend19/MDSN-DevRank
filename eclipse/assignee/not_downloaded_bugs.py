import pickle
from urllib import request
from local_settings_eclipse import db


def fetch_bugs(year: int):
    with db:
        cur = db.cursor()
        cur.execute("select distinct bug_id from bugs where bug_status='CLOSED' and "
                    "resolution='FIXED' and year(convert(creation_ts, datetime)) =" + str(year))

        bugs = []
        for i in cur.fetchall():
            bugs.append(i[0])

        url = "https://bugs.eclipse.org/bugs/show_activity.cgi?id="
        nd = []

        cnt = len(bugs)
        for i in bugs:
            print("Remaining", cnt)

            try:
                request.urlretrieve(url + str(i), "bug_html/" + str(i) + ".html")
                cnt -= 1
            except Exception:
                print("Exception : " + str(i))
                nd.append(i)

        print(nd)
        with open("nd" + str(i) + ".txt", 'wb') as fp:
            pickle.dump(nd, fp)


years = [2001, 2002, 2003, 2004, 2005, 2006, 2007]

for yr in years:
    fetch_bugs(yr)
