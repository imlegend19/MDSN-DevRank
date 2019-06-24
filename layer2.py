import pymysql
import json

db = pymysql.connect(host='localhost',
                     user='mahen',
                     password='#imlegend19',
                     db='master')

with db:
    print("Connected to db!")
    cur = db.cursor()

    print("Fetching distinct product_id's...")
    cur.execute("SELECT DISTINCT product_id FROM bug")

    products = []
    for i in cur.fetchall():
        products.append(i[0])

    # cur.execute("SELECT DISTINCT bug_id FROM comment GROUP BY bug_id HAVING COUNT(*) > 1")
    #
    # bug_id = []
    # for i in cur.fetchall():
    #     bug_id.append(i[0])

    product_bug = {}

    print("Setting up product-bug...")
    for i in products:
        print("Ongoing", i)
        cur.execute("SELECT bug_id FROM bug WHERE product_id=" + str(i))

        bugs = []
        for j in cur.fetchall():
            bugs.append(j[0])

        product_bug[i] = bugs

    with open('layer2_product_bug.txt', 'w') as file:
        file.write(json.dumps(product_bug))
