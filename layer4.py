import pymysql
import json

db = pymysql.connect(host='localhost',
                     user='mahen',
                     password='#imlegend19',
                     db='master')

"""
Layer 4 Network: 

Edge between developers who commented on 2 different bugs which belong to same operating system.

Dataset Used : gnomebug
Table : bug
"""
with db:
    print("Connected to db!")
    cur = db.cursor()

    cur.execute("select distinct bug_id, op_sys from bug")

    os_bug = {}

    print("Fetching and setting up dict...")
    for i in cur.fetchall():
        if i[1].strip() not in os_bug.keys():
            os_bug[i[1].strip()] = [i[0]]
        else:
            val = os_bug[i[1].strip()]
            val.append(i[0])
            os_bug[i[1].strip()] = val

    print("Setup succeeded!")

    with open('layer4_os_bug.txt', 'w') as file:
        file.write(json.dumps(os_bug))

    print("Process complete!")
