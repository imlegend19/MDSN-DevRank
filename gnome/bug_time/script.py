import pickle
from datetime import datetime, timedelta

from local_settings import db

PRODUCTS = [90, 186, 214, 76, 13, 34, 279, 39, 239, 87]

intervals = (
    ('days', 86400),  # 60 * 60 * 24
    ('hours', 3600),  # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


with db:
    print("Connected to db!")
    cur = db.cursor()

    prod_time = {}

    for i in PRODUCTS:
        print("Ongoing product", i)
        cur.execute("SELECT creation_ts, delta_ts FROM test_bug_fixed_closed WHERE product_id=" + str(i))

        difference = []

        total = 0
        for j in cur.fetchall():
            f = "%Y-%m-%d %H:%M:%S"

            srt = datetime.strptime(j[0].strip(), f)
            end = datetime.strptime(j[1].strip(), f)

            diff = (end - srt).total_seconds() / 60

            difference.append(diff)
            total += 1

        prod_time[i] = sum(difference) / total

    print(prod_time)

    with open('product_avg_time.txt', 'wb') as fp:
        pickle.dump(prod_time, fp)

    print("Time Format dd:hh:mm:ss")

    for i in prod_time.values():
        t = timedelta(seconds=i)
        print(str(t.days) + ':' + str(timedelta(seconds=t.seconds)))
