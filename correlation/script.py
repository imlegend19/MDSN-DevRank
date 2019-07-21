import pickle

import openpyxl


def fetch_file(path):
    with open(path, 'rb') as fp:
        file = pickle.load(fp)

    return file


RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/"

wb = openpyxl.Workbook()
sheet = wb.active

titles = ["Assignee Id", "Assignee", "L1 Centrality", "L2-A Centrality", "L2-B Centrality", "L3 Centrality",
          "L4 Centrality", "Global Centrality A", "Global Centrality B", "Avg Fixed Time"]

sheet.append(titles)
sheet.append(["" for i in range(len(titles))])

who_assignee = {v: k for k, v in fetch_file(RELATIVE_PATH + "assignee_bug/assignee_who.txt").items()}

who = []
for i in who_assignee:
    who.append(i)

l1_centrality = fetch_file(RELATIVE_PATH + "layers/l1_centrality.txt")
l2_d1_centrality = fetch_file(RELATIVE_PATH + "layers/l2_d1_centrality.txt")
l2_d2_centrality = fetch_file(RELATIVE_PATH + "layers/l2_d2_centrality.txt")
l3_centrality = fetch_file(RELATIVE_PATH + "layers/l3_centrality.txt")
l4_centrality = fetch_file(RELATIVE_PATH + "layers/l4_centrality.txt")
global_d1_centrality = fetch_file(RELATIVE_PATH + "global_eigenvector/EigenVector/definition_1/global_ev_dict.txt")
global_d2_centrality = fetch_file(RELATIVE_PATH + "global_eigenvector/EigenVector/definition_2/global_ev_dict.txt")
avg_fixed_time = fetch_file(RELATIVE_PATH + "assignee_bug/assignee_avg_fixed_time.txt")
print(avg_fixed_time)

for i in who:
    w_a = who_assignee[i]

    try:
        l1 = l1_centrality[i]
    except KeyError:
        l1 = '-'

    try:
        l2_d1 = l2_d1_centrality[i]
    except KeyError:
        l2_d1 = '-'

    try:
        l2_d2 = l2_d2_centrality[i]
    except KeyError:
        l2_d2 = '-'

    try:
        l3 = l3_centrality[i]
    except KeyError:
        l3 = '-'

    try:
        l4 = l4_centrality[i]
    except KeyError:
        l4 = '-'

    try:
        gl_a = global_d1_centrality[i]
    except KeyError:
        gl_a = '-'

    try:
        gl_b = global_d2_centrality[i]
    except KeyError:
        gl_b = '-'

    avg = avg_fixed_time[i]
    row = [i, w_a, l1, l2_d1, l2_d2, l3, l4, gl_a, gl_b, avg]

    sheet.append(row)

wb.save("correlation.xlsx")
