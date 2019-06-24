import json
from itertools import permutations

import pymysql
import openpyxl

db = pymysql.connect(host='localhost',
                     user='mahen',
                     password='#imlegend19',
                     db='master')

with db:
    print("Connected to db!")
    cur = db.cursor()

    # print("Fetching all rows...")
    # cur.execute("SELECT * FROM comment")
    #
    # rows = cur.fetchall()

    bug_who = {}

    print("Setting up dict for who_id's who have commented on same bug...")

    cur.execute("SELECT bug_id, who_id FROM comment")

    # FMT = '%H:%M:%S'
    # start = datetime.now().time()

    for i in cur.fetchall():
        if i[0] in bug_who.keys():
            val = bug_who[i[0]]
            val.add(i[1])
            bug_who[i[0]] = val
        else:
            bug_who[i[0]] = {i[1]}

    print("Fetched!")

    print("Setting up excel sheet...")
    wb = openpyxl.Workbook()
    sheet = wb.active

    print("Writing values to sheet...")
    edges = set()
    for i in bug_who.values():
        if len(list(i)) > 1:
            edg = list(permutations(list(i), 2))
            for j in edg:
                edges.add(j)

    with open('layer1_edges.txt', 'w') as file:
        file.write(str(edges))

    print("Process Competed!")
