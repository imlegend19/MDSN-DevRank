import pickle
import openpyxl
from local_settings_eclipse import db


def fetch_file(path):
    with open(path, 'rb') as fp:
        file = pickle.load(fp)

    return file


RELATIVE_PATH = "/home/imlegend19/PycharmProjects/Research - Data Mining/eclipse/"

wb = openpyxl.Workbook()
sheet = wb.active

titles = ["Assignee Id", "L1 Centrality", "L2-A Centrality", "L2-B Centrality", "L3 Centrality",
          "Global Centrality A", "Global Centrality B", "Avg Fixed Time", "Reopened Percent",
          "Assignee Component", "Total Bugs", "Priority", "Severity"]

sheet.append(titles)
sheet.append(["" for i in range(len(titles))])

with db:
    cur = db.cursor()
    cur.execute("SELECT DISTINCT assigned_to FROM test_bugs_fixed_closed "
                "WHERE assigned_to IN (SELECT who FROM test_longdescs_fixed_closed)")

who = []
for i in cur.fetchall():
    who.append(i[0])

l1_centrality = fetch_file(RELATIVE_PATH + "layers/l1_centrality.txt")
l2_d1_centrality = fetch_file(RELATIVE_PATH + "layers/l2_d1_centrality.txt")
l2_d2_centrality = fetch_file(RELATIVE_PATH + "layers/l2_d2_centrality.txt")
l3_centrality = fetch_file(RELATIVE_PATH + "layers/l3_centrality.txt")
global_d1_centrality = fetch_file(RELATIVE_PATH + "global_eigenvector/EigenVector/definition_1/global_ev_dict.txt")
global_d2_centrality = fetch_file(RELATIVE_PATH + "global_eigenvector/EigenVector/definition_2/global_ev_dict.txt")
avg_fixed_time = fetch_file(RELATIVE_PATH + "assignee/assignee_avg_fixed_time.txt")
reopened_percent = fetch_file(RELATIVE_PATH + "assignee/assignee_reopened.txt")
assignee_comp = fetch_file(RELATIVE_PATH + "assignee/assignee_component.txt")
tot_bugs = fetch_file(RELATIVE_PATH + "assignee/assignee_total_bugs.txt")
priority = fetch_file(RELATIVE_PATH + "assignee/assignee_priority_count.txt")
severity = fetch_file(RELATIVE_PATH + "assignee/assignee_severity_count.txt")

for i in who:
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
        gl_a = global_d1_centrality[i]
    except KeyError:
        gl_a = '-'

    try:
        gl_b = global_d2_centrality[i]
    except KeyError:
        gl_b = '-'

    try:
        avg = avg_fixed_time[i].days * 24 + avg_fixed_time[i].seconds / 3600
    except KeyError:
        avg = '-'
        print(i)

    rp = (reopened_percent[i][0] / reopened_percent[i][1]) * 100
    comp = assignee_comp[i]
    bugs = tot_bugs[i]
    pri = str(priority[i])
    sev = str(severity[i])

    row = [i, l1, l2_d1, l2_d2, l3, gl_a, gl_b, avg, rp, comp, bugs, pri, sev]

    sheet.append(row)

wb.save("correlation_eclipse_1.xlsx")
print("Finished!")
