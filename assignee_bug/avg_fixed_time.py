import pickle

import datetime

with open('assignee_fixed_time.txt', 'rb') as fp:
    assignee_fixed_time = pickle.load(fp)

assignee_avg_fixed_time = {}

for i in assignee_fixed_time:
    j = assignee_fixed_time[i]
    assignee_avg_fixed_time[i] = datetime.timedelta(seconds=((j[0].days * 86400 + j[0].seconds) / j[1]))

with open('assignee_avg_fixed_time.txt', 'wb') as fp:
    pickle.dump(assignee_avg_fixed_time, fp)
