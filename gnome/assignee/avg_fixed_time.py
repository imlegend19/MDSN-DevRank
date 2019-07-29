import pickle

import datetime

with open('assignee_first_fixed_time.txt', 'rb') as fp:
    assignee_fixed_time = pickle.load(fp)

with open('assignee_who.txt', 'rb') as fp:
    assignee_who = pickle.load(fp)

assignee_avg_fixed_time = {}

for i in assignee_fixed_time:
    j = assignee_fixed_time[i]
    assignee_avg_fixed_time[assignee_who[i]] = datetime.timedelta(seconds=((j[0].days * 86400 + j[0].seconds) / j[1]))

with open('assignee_avg_first_fixed_time.txt', 'wb') as fp:
    pickle.dump(assignee_avg_fixed_time, fp)

print(assignee_avg_fixed_time)
