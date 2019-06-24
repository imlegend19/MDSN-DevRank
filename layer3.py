import pymysql
import json

db = pymysql.connect(host='localhost',
                     user='mahen',
                     password='#imlegend19',
                     db='master')

with db:
    print("Connected to db!")
    cur = db.cursor()

    cur.execute("select distinct bug_id, component from bug")

    comp_bug = {}

    print("Fetching and setting up dict...")
    for i in cur.fetchall():
        if i[1].strip() not in comp_bug.keys():
            comp_bug[i[1].strip()] = [i[0]]
        else:
            val = comp_bug[i[1].strip()]
            val.append(i[0])
            comp_bug[i[1].strip()] = val

    print("Setup succeeded!")

    with open('layer3_component_bug.txt', 'w') as file:
        file.write(json.dumps(comp_bug))

    print("Process complete!")
